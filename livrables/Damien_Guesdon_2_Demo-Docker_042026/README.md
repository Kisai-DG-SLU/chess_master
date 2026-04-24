# Livrable 2 - Démo Docker

**Projet :** ChessMasterAI - Agent IA pour l'apprentissage des échecs (FFE)
**Auteur :** Damien Guesdon
**Date :** 04/2026

## Démonstration de l'Agent IA

### Prérequis

- Docker et Docker Compose installés
- Pixi (gestionnaire d'environnements)

### Démarrage

```bash
# Cloner le dépôt
git clone https://github.com/Kisai-DG-SLU/chess_master.git
cd chess_master

# Installer les dépendances
pixi install

# Build et démarrer tous les services
pixi run docker-compose up --build
```

### Services déployés

| Service | Port | Description |
|---------|------|-------------|
| API FastAPI | 8000 | Backend avec LangGraph, Lichess, Stockfish, Milvus |
| Frontend Angular | 4201 | Interface avec échiquier ngx-chessboard |
| Milvus | 19530 | Base vectorielle RAG |
| MongoDB | 27017 | Base NoSQL (utilisateurs, parties) |
| Stockfish | 8080 | Moteur d'échecs |

### Accès

- **Frontend :** http://localhost:4201
- **API Swagger :** http://localhost:8000/docs
- **Health check :** http://localhost:8000/health

### Fonctionnalités démontrées

1. **Échiquier interactif** avec ngx-chessboard
2. **Analyse de position** via Stockfish (évaluation + meilleur coup)
3. **Recherche théorique** via API Lichess (coups théoriques)
4. **RAG vectoriel** via Milvus (contexte des ouvertures)
5. **Recommandations** d'ouvertures adaptées
6. **Recherche vidéo** YouTube (ressources pédagogiques)

### Arrêt

```bash
pixi run docker-compose down
```

### Positions de démonstration

- **Ruy Lopez :** `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3`
- **Sicilienne :** `rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKB1R w KQkq c6 0 2`
