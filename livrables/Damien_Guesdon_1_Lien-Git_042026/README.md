# Livrable 1 - Dépôt Git

**Projet :** ChessMasterAI - Agent IA pour l'apprentissage des échecs (FFE)
**Auteur :** Damien Guesdon
**Date :** 04/2026
**Projet ID :** P13

## Lien Git

https://github.com/Kisai-DG-SLU/chess_master

## Contenu du dépôt

Le dépôt contient l'ensemble du code source du POC :

- `agent/` - Implémentation LangGraph (workflow décisionnel)
- `api/` - API FastAPI avec endpoints REST
- `rag/` - Système RAG avec Milvus (base vectorielle)
- `mongodb/` - Intégration MongoDB (utilisateurs, parties)
- `frontend-angular/` - Interface Angular avec ngx-chessboard
- `vision/` - Module Computer Vision (conception)
- `docker-compose.yml` - Orchestration Docker Compose
- `Dockerfile` - Image Python pour l'API
- `NOTE_CADRAGE.md` - Note de cadrage complète
- `NOTE_VISION.md` - Note bénéfices/limites système vidéo
- `ARCHITECTURE_MCP.md` - Architecture MCP détaillée
- `README.md` - Documentation complète du projet

## Technologies

- **Backend :** Python 3.10+, FastAPI, LangGraph
- **Frontend :** Angular, ngx-chessboard
- **Base de données :** Milvus (vectoriel), MongoDB (NoSQL)
- **Moteur d'échecs :** Stockfish
- **Conteneurisation :** Docker Compose
- **API externes :** Lichess, YouTube

## Installation

```bash
git clone https://github.com/Kisai-DG-SLU/chess_master.git
cd chess_master
pixi install
pixi run docker-compose up --build
```

## Accès

- API : http://localhost:8000
- Frontend Angular : http://localhost:4201
- Documentation API : http://localhost:8000/docs
