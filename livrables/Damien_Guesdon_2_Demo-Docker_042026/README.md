# Livrable 2 - Démo Docker

**Projet :** ChessMasterAI - Agent IA pour l'apprentissage des échecs (FFE)
**Auteur :** Damien Guesdon
**Date :** 04/2026

## Démonstration de l'Agent IA

### Prérequis

- Docker et Docker Compose installés
- Pixi (gestionnaire d'environnements)
- Clés API dans un fichier `.env` :
  - `MISTRAL_API_KEY` (pour LangGraph)
  - `YOUTUBE_API_KEY` (pour recherche vidéos)

### Démarrage

```bash
# Cloner le dépôt
git clone https://github.com/Kisai-DG-SLU/chess_master.git
cd chess_master

# Installer les dépendances
pixi install

# Créer le fichier .env avec vos clés API
echo "MISTRAL_API_KEY=your_key" > .env
echo "YOUTUBE_API_KEY=your_key" >> .env

# Build et démarrer tous les services
pixi run docker-compose up --build
```

### Services déployés

| Service | Port | Description |
|---------|------|-------------|
| API FastAPI | 8000 | Backend LangGraph, Stockfish, RAG, YouTube, MongoDB |
| Frontend Angular | 4200 | Interface 3 colonnes avec échiquier ngx-chessboard |
| Milvus | 19530 | Base vectorielle RAG |
| MongoDB | 27017 | Base NoSQL (utilisateurs, parties) |
| Stockfish | 8080 | Moteur d'échecs |

### Accès

- **Frontend :** http://localhost:4200
- **API Swagger :** http://localhost:8000/docs
- **Health check :** http://localhost:8000/health

### Fonctionnalités démontrées

#### 1. Échiquier interactif (Colonne 1)
- Échiquier ngx-chessboard de 400x400px
- Boutons : Analyser cette position, Reinitialiser
- Positions rapides : Ruy Lopez, Sicilienne
- Sélecteur de niveau (debutant, intermediaire, avance)
- Profil compact : creation de compte utilisateur, sauvegarde de partie

#### 2. Analyse de position (Colonne 2)
- **Evaluation Stockfish** : meilleur coup + score (en centipions ou mat)
- **Theorie** : recherche dans la base de connaissances RAG
- **Contexte** : informations sur les ouvertures similaires
- **Recommandations** : ouvertures proposees adaptees au niveau du joueur

#### 3. Vidéos YouTube (Colonne 3)
- Recherche de vidéos FR sur l'ouverture detectee
- Filtres : durée max 20 minutes, tri par rating puis vues
- 2 vidéos par recommandation d'ouverture
- Quota API YouTube avec barre de progression
- Stats de filtrage (durees rejetees, chaines, doublons)

#### 4. Gestion utilisateurs (MongoDB)
- Creation de compte utilisateur
- Sauvegarde des parties analysees
- Historique des parties sauvegardees

### Demo live (1 minute)

1. **Montrer l'interface** - Echiquier ngx-chessboard, 3 colonnes responsive
2. **Cliquer "Ruy Lopez"** - Position pre-chargee sur l'echiquier
3. **Cliquer "Analyser"** - Affichage de l'evaluation Stockfish, theorie, recommandations
4. **Montrer les vidéos** - 2 vidéos FR par ouverture, avec quotas
5. **Montrer MongoDB** - Creation de compte + sauvegarde de partie

### Arret

```bash
pixi run docker-compose down
```

### Positions de demonstration

- **Ruy Lopez :** `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3`
- **Sicilienne :** `rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKB1R w KQkq c6 0 2`
