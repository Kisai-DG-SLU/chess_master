# Livrable 1 - Dépôt Git

**Projet :** ChessMasterAI - Agent IA pour l'apprentissage des échecs (FFE)
**Auteur :** Damien Guesdon
**Date :** 04/2026
**Projet ID :** P13

## Lien Git

https://github.com/Kisai-DG-SLU/chess_master

## Contenu du dépôt

Le dépôt contient l'ensemble du code source du POC :

```
chess_master/
├── agent/                    # LangGraph agent (workflow décisionnel)
│   ├── graph.py              # Graph LangGraph (analyze → theory → recommend)
│   ├── state.py              # Types d'état de l'agent
│   └── tools.py              # Outils (Stockfish, théorie, recommandations, RAG)
├── api/                      # API FastAPI
│   └── main.py               # Endpoints REST (analyze, videos, users, games, etc.)
├── rag/                      # Système RAG
│   └── vector_store.py       # Store vectoriel en mémoire (fallback sans Milvus)
├── mongodb/                  # Intégration MongoDB
│   └── models.py             # Modèles utilisateurs et parties
├── frontend-angular/          # Interface Angular
│   ├── src/app/              # Composants Angular
│   │   ├── app.component.ts  # Composant principal
│   │   ├── app.component.html # Template 3 colonnes (échiquier, analyse, vidéos)
│   │   └── app.component.scss # Styles
│   └── Dockerfile            # Image Docker pour le frontend
├── vision/                   # Module Computer Vision (POC)
│   └── video_to_fen.py       # Extraction FEN depuis vidéo
├── docker-compose.yml        # Orchestration Docker (5 services)
├── Dockerfile                # Image Python pour l'API
├── pixi.toml                 # Configuration Pixi (dépendances)
├── NOTE_CADRAGE.md           # Note de cadrage (architecture + coûts)
├── NOTE_VISION.md            # Note bénéfices/limites système vidéo
├── ARCHITECTURE_MCP.md       # Architecture MCP détaillée
└── README.md                 # Documentation complète
```

## Stack technique

- **Backend :** Python 3.10+, FastAPI, LangGraph
- **Frontend :** Angular 19, ngx-chessboard
- **Base de données :** Milvus (vectoriel, RAG), MongoDB (NoSQL)
- **Moteur d'échecs :** Stockfish
- **Conteneurisation :** Docker Compose
- **API externes :** YouTube Data v3, Lichess

## Fonctionnalités implémentées

### Partie 1 - Développement POC
1. **Orchestration LangGraph** - Workflow décisionnel : analyse → théorie → recommandations
2. **Analyse de position** - Stockfish (évaluation + meilleur coup)
3. **Recherche théorique** - Base de connaissances locale (RAG vectoriel)
4. **Recommandations** - Ouvertures adaptées au niveau du joueur
5. **Interface Angular** - Échiquier interactif ngx-chessboard, 3 colonnes responsive
6. **Recherche vidéo YouTube** - Filtres FR, durée max 20min, tri par rating puis vues
7. **Gestion utilisateurs** - MongoDB (création, parties sauvegardées)
8. **Conteneurisation** - Docker Compose (5 services : API, Angular, Milvus, MongoDB, Stockfish)

### Partie 2 - Étude avancée (conception)
1. **Système vidéo Computer Vision** - Extraction FEN depuis vidéo (YOLO + CNN)
2. **Architecture MCP** - Model Context Protocol pour modularité
3. **Business Case** - Étude de faisabilité, chiffrage Build + OPEX

## Installation

```bash
git clone https://github.com/Kisai-DG-SLU/chess_master.git
cd chess_master
pixi install
pixi run docker-compose up --build
```

## Accès

- **Frontend Angular :** http://localhost:4200
- **API FastAPI :** http://localhost:8000
- **Documentation API Swagger :** http://localhost:8000/docs
- **Health check :** http://localhost:8000/health
