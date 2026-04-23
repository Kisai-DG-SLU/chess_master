import cv2
import numpy as np
from typing import List, Tuple, Optional
import chess
import chess.svg

class ChessboardDetector:
    """Module de détection d'échiquier et extraction FEN depuis vidéo"""
    
    def __init__(self):
        self.chessboard_corners = None
        self.square_positions = []
        
    def extract_frame(self, video_path: str, timestamp: float = 0.0) -> np.ndarray:
        """Extrait une frame à un timestamp donné"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(timestamp * fps)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError(f"Impossible de lire la frame à {timestamp}s")
        return frame
    
    def detect_chessboard(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """Détecte l'échiquier dans l'image"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détection de coins avec Harris
        corners = cv2.cornerHarris(gray, 5, 3, 0.04)
        corners = cv2.dilate(corners, None)
        
        # Seuillage pour trouver les coins forts
        ret, corners = cv2.threshold(corners, 0.01 * corners.max(), 255, 0)
        corners = np.uint8(corners)
        
        # Trouver les contours
        contours, _ = cv2.findContours(corners, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Prendre le plus grand contour (supposé être l'échiquier)
            largest = max(contours, key=cv2.contourArea)
            epsilon = 0.02 * cv2.arcLength(largest, True)
            approx = cv2.approxPolyDP(largest, epsilon, True)
            
            if len(approx) == 4:
                return approx.reshape(4, 2)
        
        return None
    
    def perspective_transform(self, frame: np.ndarray, corners: np.ndarray) -> np.ndarray:
        """Redresse l'échiquier avec transformation de perspective"""
        # Points de destination (échiquier carré 800x800)
        dst_points = np.array([[0, 0], [800, 0], [800, 800], [0, 800]], dtype=np.float32)
        
        # Calcul de la transformation de perspective
        matrix = cv2.getPerspectiveTransform(corners.astype(np.float32), dst_points)
        warped = cv2.warpPerspective(frame, matrix, (800, 800))
        
        return warped
    
    def identify_pieces(self, warped_board: np.ndarray) -> List[List[Optional[str]]]:
        """Identifie les pièces sur l'échiquier"""
        board_state = [[None for _ in range(8)] for _ in range(8)]
        square_size = 100
        
        for row in range(8):
            for col in range(8):
                x1 = col * square_size
                y1 = row * square_size
                square = warped_board[y1:y1+square_size, x1:x1+square_size]
                
                # Analyser la couleur moyenne pour détecter une pièce
                avg_color = np.mean(square)
                
                # Logique simplifiée : si la case est proche du blanc, pas de pièce
                # Dans une vraie implémentation, utiliser un modèle CNN
                if avg_color < 200:  # Supposons que c'est une pièce
                    # Ici, on devrait utiliser un classifieur
                    # Pour le POC, on met juste 'P' (pion) par défaut
                    board_state[row][col] = 'P'
        
        return board_state
    
    def board_to_fen(self, board_state: List[List[Optional[str]]]) -> str:
        """Convertit l'état de l'échiquier en notation FEN"""
        fen_rows = []
        
        for row in board_state:
            empty_count = 0
            fen_row = ""
            
            for piece in row:
                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            fen_rows.append(fen_row)
        
        # FEN de base (sans informations de roque, en passant, etc.)
        return "/".join(fen_rows) + " w KQkq - 0 1"
    
    def analyze_video(self, video_path: str, timestamps: List[float] = None) -> List[Tuple[float, str]]:
        """Analyse une vidéo et extrait les positions FEN à différents moments"""
        if timestamps is None:
            timestamps = [0.0, 5.0, 10.0]  # Par défaut
        
        results = []
        
        for timestamp in timestamps:
            try:
                frame = self.extract_frame(video_path, timestamp)
                corners = self.detect_chessboard(frame)
                
                if corners is not None:
                    warped = self.perspective_transform(frame, corners)
                    board_state = self.identify_pieces(warped)
                    fen = self.board_to_fen(board_state)
                    results.append((timestamp, fen))
                else:
                    results.append((timestamp, "Échiquier non détecté"))
            
            except Exception as e:
                results.append((timestamp, f"Erreur: {str(e)}"))
        
        return results


# Exemple d'utilisation
if __name__ == "__main__":
    detector = ChessboardDetector()
    
    # Pour tester avec une image au lieu d'une vidéo
    # frame = cv2.imread("chessboard.jpg")
    # corners = detector.detect_chessboard(frame)
    # if corners is not None:
    #     warped = detector.perspective_transform(frame, corners)
    #     board = detector.identify_pieces(warped)
    #     fen = detector.board_to_fen(board)
    #     print(f"Position FEN: {fen}")
    
    print("Module de vision prêt. Utiliser analyze_video() pour analyser une vidéo.")
