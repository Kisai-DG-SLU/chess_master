from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import requests

# Try to import agent graph, fallback if fails
try:
    import agent.graph as agent_graph
except Exception as e:
    agent_graph = None
    print(f"Warning: Could not import agent.graph: {e}")

from mongodb.models import MongoDB


app = FastAPI(title="Chess Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    position: str
    player_level: Optional[str] = "intermediate"


class AnalyzeResponse(BaseModel):
    position: str
    analysis: dict
    theory: Optional[str]
    recommendations: list[str]


@app.get("/")
def root():
    return {"message": "Chess Agent API - FFE Training Assistant"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/moves")
def get_theoretical_moves(fen: str):
    """Récupère les coups théoriques depuis une base de données locale."""
    # Base de données des ouvertures courantes
    openings_db = {
        "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": {
            "name": "Ruy Lopez",
            "moves": [
                {"san": "Bb5", "uci": "f1b5", "percentage": 85},
                {"san": "d3", "uci": "d2d3", "percentage": 10},
                {"san": "c3", "uci": "c2c3", "percentage": 5},
            ]
        },
        "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2": {
            "name": "Sicilian Defense",
            "moves": [
                {"san": "Nf3", "uci": "g1f3", "percentage": 80},
                {"san": "Bb5", "uci": "f1b5", "percentage": 10},
                {"san": "c3", "uci": "c2c3", "percentage": 5},
            ]
        }
    }
    
    if fen in openings_db:
        data = openings_db[fen]
        return {"fen": fen, "moves": data["moves"], "opening": data["name"]}
    
    return {"fen": fen, "moves": [], "opening": "Unknown", "message": "Position non reconnue dans la base d'ouvertures"}


@app.get("/api/v1/evaluate")
def evaluate_position(fen: str):
    """Évalue la position via Stockfish."""
    try:
        import stockfish
        sf = stockfish.Stockfish(path="/usr/games/stockfish")
        sf.set_fen_position(fen)
        best_move = sf.get_best_move()
        eval_info = sf.get_evaluation()
        return {
            "fen": fen,
            "best_move": best_move,
            "evaluation": eval_info
        }
    except Exception as e:
        return {"fen": fen, "error": str(e)}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        if agent_graph:
            result = agent_graph.run_agent(request.position)
        else:
            # Fallback when agent.graph is not available
            result = {
                "position": request.position,
                "analysis": {"result": "Stockfish analysis unavailable"},
                "theory": "Analysis module loading...",
                "recommendations": [
                    "Ruy Lopez - 1.e4 e5 2.Nf3 Nc6 3.Bb5",
                    "Sicilian Defense - 1.e4 c5",
                    "Queen's Gambit - 1.d4 d5 2.c4"
                ]
            }
        
        return AnalyzeResponse(
            position=result.get("position", request.position),
            analysis=result.get("analysis", {}),
            theory=result.get("theory"),
            recommendations=result.get("recommendations", [])
        )
    except Exception as e:
        return AnalyzeResponse(
            position=request.position,
            analysis={"error": str(e)},
            theory="Analysis error occurred",
            recommendations=["Ruy Lopez - 1.e4 e5 2.Nf3 Nc6 3.Bb5"]
        )


@app.get("/openings")
def get_openings():
    return {
        "openings": [
            {"name": "Ruy Lopez", "moves": "1.e4 e5 2.Nf3 Nc6 3.Bb5", "style": "tactical"},
            {"name": "Sicilian Defense", "moves": "1.e4 c5", "style": "aggressive"},
            {"name": "Queen's Gambit", "moves": "1.d4 d5 2.c4", "style": "positional"},
            {"name": "King's Indian", "moves": "1.d4 Nf6 2.c4 g6", "style": "aggressive"},
            {"name": "English Opening", "moves": "1.c4", "style": "flexible"}
        ]
    }


@app.get("/vector-search")
def vector_search(query: str, top_k: int = 3):
    """Recherche vectorielle dans la base Milvus."""
    try:
        from rag.vector_store import search_openings
        results = search_openings(query, top_k=top_k)
        return {"results": results, "query": query}
    except Exception as e:
        return {"results": [], "error": str(e)}


# MongoDB routes
mongodb = MongoDB()


class UserCreate(BaseModel):
    username: str
    email: str
    level: str = "beginner"


class GameCreate(BaseModel):
    user_id: str
    position: str
    analysis: dict
    recommendations: list[str]


@app.post("/users")
def create_user(user: UserCreate):
    try:
        user_id = mongodb.create_user(user.dict())
        return {"user_id": user_id, "message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        user = mongodb.get_user(user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/games")
def save_game(game: GameCreate):
    try:
        game_id = mongodb.save_game(game.dict())
        return {"game_id": game_id, "message": "Game saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/games")
def get_user_games(user_id: str, limit: int = 10):
    try:
        games = mongodb.get_user_games(user_id, limit)
        return {"games": games}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/videos")
def search_videos(opening: str):
    """Recherche vidéos YouTube via l'API officielle."""
    try:
        import os
        from urllib.parse import quote
        
        api_key = os.getenv("YOUTUBE_API_KEY", "AIzaSyCScqzwMhEK5iKyouXH7PhivnKm3q9dl0k")
        query = quote(f"{opening} chess opening")
        url = f"https://www.googleapis.com/youtube/v3/search?q={query}&part=snippet&type=video&maxResults=5&key={api_key}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "error" in data:
            return {
                "videos": [],
                "opening": opening,
                "error": data["error"]["message"],
                "debug": {"status_code": response.status_code}
            }
        
        items = data.get("items", [])
        if not items:
            return {
                "videos": [],
                "opening": opening,
                "debug": {
                    "query": f"{opening} chess opening",
                    "total_results": data.get("pageInfo", {}).get("totalResults", 0),
                    "message": "Aucune vidéo trouvée."
                }
            }
        
        videos = []
        for item in items:
            videos.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"][:200],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
            })
        
        return {"videos": videos, "opening": opening}
    except Exception as e:
        return {"videos": [], "error": str(e)}
