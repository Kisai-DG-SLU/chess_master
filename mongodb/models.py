from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List, Dict, Any

class MongoDB:
    def __init__(self, uri: str = "mongodb://mongodb:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client["chess_master"]
        self.users = self.db["users"]
        self.games = self.db["games"]
        
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Crée un nouvel utilisateur"""
        user_data["created_at"] = datetime.utcnow()
        result = self.users.insert_one(user_data)
        return str(result.inserted_id)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un utilisateur par ID"""
        from bson import ObjectId
        return self.users.find_one({"_id": ObjectId(user_id)})
    
    def save_game(self, game_data: Dict[str, Any]) -> str:
        """Sauvegarde une partie"""
        game_data["created_at"] = datetime.utcnow()
        result = self.games.insert_one(game_data)
        return str(result.inserted_id)
    
    def get_user_games(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère les parties d'un utilisateur"""
        from bson import ObjectId
        return list(self.games.find(
            {"user_id": ObjectId(user_id)}
        ).sort("created_at", -1).limit(limit))
