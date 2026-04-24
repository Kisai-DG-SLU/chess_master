from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import requests
import agent.graph as agent_graph
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
    """Récupère les coups théoriques depuis l'API Lichess."""
    try:
        import urllib.parse
        escaped_fen = urllib.parse.quote(fen, safe='/')
        url = f"https://lichess.org/api/explorer?fen={escaped_fen}&mode=historical"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            moves = []
            for m in data.get("moves", []):
                moves.append({
                    "uci": m.get("uci", ""),
                    "san": m.get("san", ""),
                    "percentage": m.get("percentage", 0),
                    "games": m.get("white", 0) + m.get("black", 0)
                })
            return {"fen": fen, "moves": moves}
        return {"fen": fen, "moves": [], "error": "Lichess API unavailable"}
    except Exception as e:
        return {"fen": fen, "moves": [], "error": str(e)}


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
        result = agent_graph.run_agent(request.position)
        
        return AnalyzeResponse(
            position=result.get("position", request.position),
            analysis=result.get("analysis", {}),
            theory=result.get("theory"),
            recommendations=result.get("recommendations", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        from googleapiclient.discovery import build
        import os
        
        api_key = os.getenv("YOUTUBE_API_KEY", "AIzaSyCScqzwMhEK5iKyouXH7PhivnKm3q9dl0k")
        youtube = build("youtube", "v3", developerKey=api_key)
        
        search_response = youtube.search().list(
            q=f"{opening} chess opening tutorial",
            part="snippet",
            type="video",
            maxResults=5
        ).execute()
        
        videos = []
        for item in search_response.get("items", []):
            videos.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"][:200],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            })
        
        return {"videos": videos, "opening": opening}
    except Exception as e:
        return {"videos": [], "error": str(e)}
