class VectorStore:
    """In-memory vector store with keyword search - robust fallback without Milvus."""
    
    def __init__(self):
        self.openings = [
            {
                "id": 1,
                "opening_name": "Ruy Lopez",
                "moves": "1.e4 e5 2.Nf3 Nc6 3.Bb5",
                "description": "Classical opening dating to 1561. One of the most popular and theoretically important openings.",
                "keywords": ["tactical", "aggressive", "classical", "white", "minor piece"]
            },
            {
                "id": 2,
                "opening_name": "Sicilian Defense",
                "moves": "1.e4 c5",
                "description": "The most popular response to 1.e4. Leads to sharp, tactical positions. Many variations including Open, Closed, and Siciilian Defense.",
                "keywords": ["tactical", "aggressive", "sharp", "black", "counterattack"]
            },
            {
                "id": 3,
                "opening_name": "Queen's Gambit",
                "moves": "1.d4 d5 2.c4",
                "description": "One of the oldest and most respected openings. White sacrifices a pawn for better development and central control.",
                "keywords": ["positional", "solid", "white", "pawn", "control"]
            },
            {
                "id": 4,
                "opening_name": "King's Indian Defense",
                "moves": "1.d4 Nf6 2.c4 g6",
                "description": "Hypermodern opening where Black allows White to occupy the center before attacking it. Popular among aggressive players.",
                "keywords": ["aggressive", "hypermodern", "black", "attack", "dynamic"]
            },
            {
                "id": 5,
                "opening_name": "French Defense",
                "moves": "1.e4 e6",
                "description": "Solid defensive opening. Leads to varied positions with pawn structures unique to this opening.",
                "keywords": ["solid", "defensive", "black", "positional", "white attacking"]
            },
            {
                "id": 6,
                "opening_name": "Caro-Kann Defense",
                "moves": "1.e4 c6",
                "description": "Reliable response to 1.e4. Less sharp than Sicilian but leads to solid positions.",
                "keywords": ["solid", "reliable", "black", "positional", "safe"]
            },
            {
                "id": 7,
                "opening_name": "London System",
                "moves": "1.d4 Nf6 2.Bf4",
                "description": "Reliable system that can be played against almost any Black setup. Popular at all levels.",
                "keywords": ["solid", "system", "white", "beginner", "safe"]
            },
            {
                "id": 8,
                "opening_name": "Reti Opening",
                "moves": "1.Nf3 d5 2.c4",
                "description": "Hypermodern opening that controls the center with pieces rather than pawns.",
                "keywords": ["hypermodern", "flexible", "white", "piece", "control"]
            }
        ]
    
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Search openings by keywords - returns defaults if no match."""
        import random
        
        query_lower = query.lower()
        query_words = query_lower.split()
        
        results = []
        for opening in self.openings:
            score = 0
            for word in query_words:
                if len(word) > 2:
                    if word in opening["keywords"]:
                        score += 1
                    if word in opening["description"].lower():
                        score += 0.5
                    if word in opening["opening_name"].lower():
                        score += 2
            
            if score > 0:
                results.append({**opening, "score": score})
        
        if not results:
            # Fallback: return random selection of all openings
            results = [{**op} for op in self.openings]
            random.shuffle(results)
        else:
            results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]
    
    def get_all(self) -> list[dict]:
        return self.openings


vector_store = VectorStore()


def search_openings(query: str, top_k: int = 3) -> list[dict]:
    """Search function for the RAG system."""
    return vector_store.search(query, top_k)
