from typing import Callable
from langchain_core.tools import tool
import requests
import rag.vector_store as vs

@tool
def analyze_position(fen: str) -> str:
    """Analyse une position d'échecs via le moteur Stockfish."""
    try:
        import stockfish
        # Correction du chemin vers le binaire stockfish si nécessaire
        sf = stockfish.Stockfish(path="/usr/games/stockfish")
        sf.set_fen_position(fen)
        
        best_move = sf.get_best_move()
        eval_info = sf.get_evaluation()
        
        return f"Best move: {best_move}. Evaluation: {eval_info}"
    except Exception as e:
        return f"Erreur analyse : {str(e)}"

@tool  
def search_theory(position: str) -> str:
    """Recherche la théorie d'ouverture dans la base de connaissances locale."""
    try:
        # On interroge directement ton store vectoriel Milvus
        results = vs.search_openings(position, top_k=2)
        if results:
            # On construit la chaîne sans couper le texte (suppression de [:80])
            theory = "\n".join([
                f"- {r['opening_name']}: {r['moves']} ({r['description']})"
                for r in results
            ])
            return theory
        return "Aucune théorie trouvée pour cette position."
    except Exception as e:
        return f"Erreur recherche théorie : {str(e)}"

@tool
def get_recommendations(context: str) -> list[str]:
    """Obtient des recommandations d'ouvertures basées sur le contexte."""
    try:
        results = vs.search_openings(context, top_k=4)
        if results:
            return [f"{r['opening_name']} - {r['moves']}" for r in results]
    except:
        pass
    return [
        "1. e4 (Ouverture du Pion Roi)",
        "1. d4 (Ouverture du Pion Dame)",
        "1. c4 (Ouverture Anglaise)",
        "1. Nf3 (Ouverture Réti)"
    ]

@tool
def semantic_search(query: str) -> str:
    """Recherche sémantique dans la base de connaissances."""
    results = vs.search_openings(query, top_k=5)
    if not results:
        return "Aucun résultat trouvé."
    
    output = "Résultats de la recherche :\n"
    for r in results:
        output += f"\n{r['opening_name']}: {r['moves']}\n"
        output += f"  {r['description']}\n"
    
    return output