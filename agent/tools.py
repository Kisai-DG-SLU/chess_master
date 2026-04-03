from typing import Callable
from langchain_core.tools import tool
import requests
import rag.vector_store as vs


@tool
def analyze_position(fen: str) -> str:
    """Analyze a chess position using Stockfish engine.
    
    Args:
        FEN string representing the chess position
        
    Returns:
        Analysis including best move, evaluation, and depth
    """
    try:
        import stockfish
        sf = stockfish.Stockfish(path="/usr/bin/stockfish")
        sf.set_fen_position(fen)
        
        best_move = sf.get_best_move()
        eval_info = sf.get_evaluation()
        
        return f"Best move: {best_move}. Evaluation: {eval_info}"
    except Exception as e:
        return f"Error analyzing position: {str(e)}"


@tool  
def search_theory(position: str) -> str:
    """Search chess opening theory via Lichess API or local knowledge base.
    
    Args:
        FEN string or position to search
        
    Returns:
        Theory information about the opening
    """
    try:
        url = "https://lichess.org/api/book/standard"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"Theory data available. Position: {position[:50]}..."
        
        results = vs.search_openings(position, top_k=2)
        if results:
            theory = "\n".join([
                f"- {r['opening_name']}: {r['moves']} ({r['description'][:80]}...)"
                for r in results
            ])
            return theory
        return "No theory found for this position"
    except Exception as e:
        return f"Error searching theory: {str(e)}"


@tool
def get_recommendations(context: str) -> list[str]:
    """Get opening recommendations based on game context.
    
    Args:
        Context about the player and position
        
    Returns:
        List of recommended opening lines
    """
    results = vs.search_openings(context, top_k=4)
    recommendations = [f"{r['opening_name']} - {r['moves']}" for r in results]
    return recommendations if recommendations else [
        "1. e4 (King's Pawn Opening)",
        "1. d4 (Queen's Pawn Opening)",
        "1. c4 (English Opening)",
        "1. Nf3 (Reti Opening)"
    ]


@tool
def semantic_search(query: str) -> str:
    """Perform semantic search on chess opening knowledge base.
    
    Args:
        Query text to search
        
    Returns:
        Search results with descriptions
    """
    results = vs.search_openings(query, top_k=5)
    if not results:
        return "No results found"
    
    output = "Search Results:\n"
    for r in results:
        output += f"\n{r['opening_name']}: {r['moves']}\n"
        output += f"  {r['description']}\n"
    
    return output
