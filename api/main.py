from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import agent.graph as agent_graph
from mongodb.models import MongoDB


app = FastAPI(title="Chess Agent API", version="0.1.0")


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
