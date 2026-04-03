const API_URL = "http://localhost:8000";

const PIECES = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
};

const INITIAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

const OPENINGS = {
    'ruy_lopez': "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    'sicilian': "r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    'queens_gambit': "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2"
};

let currentFen = INITIAL_FEN;
let selectedSquare = null;
let isWhiteTurn = true;

function parseFen(fen) {
    const parts = fen.split(' ')[0].split('/');
    const board = [];
    
    for (let row of parts) {
        const rowArr = [];
        for (let char of row) {
            if (isNaN(char)) {
                rowArr.push(char);
            } else {
                for (let i = 0; i < parseInt(char); i++) {
                    rowArr.push('');
                }
            }
        }
        board.push(rowArr);
    }
    
    return board;
}

function renderBoard(fen) {
    const board = parseFen(fen);
    const boardEl = document.getElementById('chess-board');
    boardEl.innerHTML = '';
    
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const square = document.createElement('div');
            const isLight = (row + col) % 2 === 0;
            square.className = `square ${isLight ? 'light' : 'dark'}`;
            square.dataset.row = row;
            square.dataset.col = col;
            
            const piece = board[row][col];
            if (piece) {
                const pieceEl = document.createElement('span');
                pieceEl.className = 'piece';
                pieceEl.textContent = PIECES[piece];
                square.appendChild(pieceEl);
            }
            
            square.onclick = () => handleSquareClick(row, col);
            boardEl.appendChild(square);
        }
    }
}

function handleSquareClick(row, col) {
    if (selectedSquare === null) {
        selectedSquare = { row, col };
        highlightSquare(row, col);
    } else {
        const fromRow = selectedSquare.row;
        const fromCol = selectedSquare.col;
        
        if (isValidMove(fromRow, fromCol, row, col)) {
            const board = parseFen(currentFen);
            const piece = board[fromRow][fromCol];
            
            board[row][col] = piece;
            board[fromRow][fromCol] = '';
            
            currentFen = boardToFen(board);
            renderBoard(currentFen);
            updateFenInput();
        }
        
        clearSelection();
    }
}

function isValidMove(fromRow, fromCol, toRow, toCol) {
    const board = parseFen(currentFen);
    const piece = board[fromRow][fromCol];
    
    if (!piece) return false;
    
    const isWhite = piece === piece.toUpperCase();
    if (isWhite !== isWhiteTurn) return false;
    
    return Math.abs(toRow - fromRow) <= 1 && Math.abs(toCol - fromCol) <= 1;
}

function highlightSquare(row, col) {
    const squares = document.querySelectorAll('.square');
    squares.forEach(sq => {
        if (parseInt(sq.dataset.row) === row && parseInt(sq.dataset.col) === col) {
            sq.classList.add('selected');
        }
    });
}

function clearSelection() {
    selectedSquare = null;
    document.querySelectorAll('.square').forEach(sq => sq.classList.remove('selected'));
}

function boardToFen(board) {
    let fen = '';
    for (let row = 0; row < 8; row++) {
        let empty = 0;
        for (let col = 0; col < 8; col++) {
            const piece = board[row][col];
            if (!piece) {
                empty++;
            } else {
                if (empty > 0) {
                    fen += empty;
                    empty = 0;
                }
                fen += piece;
            }
        }
        if (empty > 0) fen += empty;
        if (row < 7) fen += '/';
    }
    
    const turn = isWhiteTurn ? 'w' : 'b';
    return `${fen} ${turn} KQkq - 0 1`;
}

function updateFenInput() {
    document.getElementById('fen-input').value = currentFen;
}

function resetBoard() {
    currentFen = INITIAL_FEN;
    isWhiteTurn = true;
    renderBoard(currentFen);
    updateFenInput();
    document.getElementById('analysis-result').innerHTML = 
        '<p class="placeholder">Lancez l\'analyse pour voir les recommandations</p>';
}

function setPosition(opening) {
    currentFen = OPENINGS[opening];
    isWhiteTurn = true;
    renderBoard(currentFen);
    updateFenInput();
}

async function analyzePosition() {
    const resultBox = document.getElementById('analysis-result');
    const level = document.getElementById('player-level').value;
    
    resultBox.innerHTML = '<p style="text-align:center;padding:50px;">🔄 Analyse en cours...</p>';
    
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                position: currentFen,
                player_level: level
            })
        });
        
        if (!response.ok) throw new Error('API Error');
        
        const data = await response.json();
        
        resultBox.innerHTML = `
            <h3 style="color:#1a5f2a;margin-bottom:15px;">📊 Résultats de l'analyse</h3>
            <div style="margin-bottom:15px;">
                <strong>Meilleur coup:</strong> ${data.analysis?.result || 'Non disponible'}
            </div>
            <div style="margin-bottom:15px;">
                <strong>Théorie:</strong> ${data.theory || 'Non disponible'}
            </div>
            <div>
                <strong>Recommandations:</strong>
                <ul style="margin-top:10px;padding-left:20px;">
                    ${data.recommendations?.map(r => `<li>${r}</li>`).join('') || '<li>Aucune recommendation</li>'}
                </ul>
            </div>
        `;
    } catch (error) {
        resultBox.innerHTML = `
            <p style="color:#c62828;text-align:center;">
                ⚠️ Erreur lors de l'analyse<br>
                <small>Vérifiez que l'API est démarrée (python -m api.main)</small>
            </p>
        `;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    renderBoard(currentFen);
    updateFenInput();
});
