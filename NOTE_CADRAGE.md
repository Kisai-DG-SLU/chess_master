# Note de Cadrage - Agent IA Échecs FFE

## 1. Résumé Exécutif

Ce projet vise à développer un agent conversationnel intelligent pour la Fédération Française des Échecs (FFE). Cet agent accompagne les jeunes joueurs dans l'apprentissage des ouvertures en orchestrant plusieurs outils : analyse de position (Stockfish), théorie (Lichess), recherche documentaire (RAG sur Milvus) et ressources pédagogiques (vidéos YouTube).

**Budget estimé :** 8 500€ - 15 000€ (Build + 12 mois OPEX)
**Durée :** 80 heures (POC)

---

## 2. Architecture Technique

### 2.1 Architecture Actuelle (POC)

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Angular)                     │
│                    ┌─────────────────┐                      │
│                    │  ngx-chessboard │                      │
│                    │   + UI Agent    │                      │
│                    └────────┬────────┘                      │
└─────────────────────────────┼────────────────────────────────┘
                              │ HTTP
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              LANGGRAPH AGENT                          │  │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────────────┐   │  │
│  │  │ Analyze │──▶│ Theory  │──▶│ Recommend       │   │  │
│  │  │ (Tool)  │   │ (Tool)  │   │ (Tool)          │   │  │
│  │  └────┬────┘   └────┬────┘   └────────┬────────┘   │  │
│  └───────┼────────────┼──────────────────┼────────────┘  │
│          │            │                  │                │
│          ▼            ▼                  ▼                │
│  ┌─────────────┐ ┌──────────┐ ┌─────────────────┐         │
│  │  Stockfish  │ │ Lichess  │ │  Milvus RAG     │         │
│  │  Engine     │ │   API    │ │  (Vector Store) │         │
│  └─────────────┘ └──────────┘ └─────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Architecture Future (MCP)

Le Model Context Protocol (MCP) permet une modularité accrue :

```
┌──────────────────────────────────────────────────────────────┐
│                      LLM (GPT-4 / Claude)                    │
└────────────────────────────┬───────────────────────────────────┘
                             │ MCP
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐    ┌───────────────┐
│ Stockfish MCP │   │  Lichess MCP  │    │  Milvus MCP   │
│   Server      │   │    Server     │    │    Server     │
│   (Tool)      │   │    (Tool)     │    │    (Tool)     │
└───────────────┘   └───────────────┘    └───────────────┘
```

---

## 3. Stack Technologique

| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| Orchestration | LangGraph | State machine pour cycles décisionnels |
| API | FastAPI | Performance, typage, async |
| Vector DB | Milvus | Scalabilité, performance recherche |
| NoSQL | MongoDB | Données utilisateurs, parties |
| Frontend | Angular | Maturité, ngx-chessboard |
| Engine | Stockfish | Meilleure engine open-source |
| Théorie | Lichess API | Base de données ouverte |
| Container | Docker Compose | Orchestration microservices |

---

## 4. Étude de Faisabilité

### 4.1 Bénéfices

| Bénéfice | Description | Impact |
|----------|-------------|--------|
| Accessibilité | Coach disponible 24/7 | Fort |
| Personnalisation | Adapté au niveau du joueur | Fort |
| Engagement | Interface interactive | Moyen |
| Coût | Réduction coaching humain | Fort |

### 4.2 Limites

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Précision | Erreurs d'analyse possibles | Validation humaine |
| Contextuel | Pas de lecture du langage corporel | Questions clarificatrices |
| Dépendance | API externes (Lichess) | Fallback local |

---

## 5. Chiffrage

### 5.1 Build (Développement)

| Poste | Coût estimé |
|-------|-------------|
| Développement backend (LangGraph, API) | 3 000€ |
| Intégration RAG (Milvus, embeddings) | 1 500€ |
| Frontend (Angular, échiquier) | 1 500€ |
| Docker & DevOps | 500€ |
| Tests & Documentation | 500€ |
| **Total Build** | **7 000€** |

### 5.2 OPEX (12 mois)

| Poste | Coût mensuel | Coût annuel |
|-------|--------------|-------------|
| Infrastructure cloud (VM + DB) | 150€ | 1 800€ |
| API Keys (OpenAI) | 200€ | 2 400€ |
| Monitoring & maintenance | 100€ | 1 200€ |
| **Total OPEX** | **450€** | **5 400€** |

### 5.3 Récapitulatif

| Scénario | Coût |
|----------|------|
| Build + 12 mois OPEX | **12 400€** |
| Build + 24 mois OPEX | **17 800€** |

---

## 6. Perspectives - Computer Vision & MCP

### 6.1 Vision Future (Système Vidéo Avancé)

**Objectif** : Résoudre la limitation des recherches textuelles YouTube (vidéos de 45 min pour 1 coup).

**Solution retenue** : Utilisation de modèles pré-entraînés sur Hugging Face, sans phase d'entraînement custom.

**Modèles disponibles** :
- `dopaul/chess_piece_detection` : Détection de pièces d'échecs, fine-tuné sur dataset échecs
- `NAKSTStudio/yolov8m-chess-piece-detection` : Modèle YOLOv8 standard, pipeline CV éprouvé

**Pipeline simplifié** :
```
Vidéo → FFmpeg (frames) → Modèle pré-entraîné (détection) → Mapping cases 8x8 → Notation FEN → Indexation Milvus
```

**Bénéfices** :
- ✅ Précision : Timestamp exact pour le coup demandé
- ✅ Pertinence : Recherche par FEN vs mots-clés
- ✅ UX : Accès direct au coup qui intéresse
- ✅ Innovation : Aucun concurrent direct sur le marché
- ✅ Coût réduit : Pas d'entraînement custom nécessaire

### 6.2 Architecture MCP (Model Context Protocol)

```
┌─────────────────────────────────┐
│         Client MCP (ChessMasterAI)        │
└─────────────┬───────────────────────┘
              │ MCP
     ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
     │  Video MCP  │  │ Vision MCP  │  │ Search MCP  │
     │   Server    │  │   Server    │  │   Server    │
     │            │  │            │  │            │
     │ Ingestion   │  │ FEN Extract │  │ FEN Search  │
     │ Stockage   │  │ Board Det.  │  │ Timestamp   │
     │ YouTube API│  │ Piece Det.  │  │ Ranking    │
     └────────────┘  └────────────┘  └────────────┘
```

**Outils exposés** :
- `find_video(fen: string, move_number: int)` → URL + timestamp
- `extract_fen(frame_id: string)` → FEN + confidence
- `detect_board(frame_id: string)` → Coordonnées

### 6.3 Composants Techniques

| Composant | Technologie | Détails |
|------------|-------------|---------|
| **Capture vidéo** | YouTube API / Upload | API quotas, formats supportés |
| **Extraction frames** | FFmpeg | 1 frame/2 sec, redimensionnement |
| **Détection échiquier & pièces** | YOLOv8 pré-entraîné (HF) | `NAKSTStudio/yolov8m-chess-piece-detection` ou `dopaul/chess_piece_detection` |
| **Génération FEN** | Algorithme coords | Mapping détection → board 8x8 → notation FEN |
| **Indexation** | Milvus | Embeddings FEN, recherche vectorielle |
| **Serveur MCP** | Python | Stdio, HTTP, WebSocket |

### 6.4 Étude de Faisabilité (Coût)

**Build (Développement)** :

| Poste | Coût estimé | Détails |
|-------|-------------|---------|
| Pipeline Vidéo | 1 500€ | FFmpeg, extraction frames, stockage S3 |
| Intégration Modèle HF | 500€ | Chargement `dopaul/chess_piece_detection` ou `NAKSTStudio/yolov8m-chess-piece-detection` |
| Mapping FEN | 500€ | Algorithme détection → board 8x8 → FEN |
| Serveur MCP & Intégration | 1 000€ | Dev serveur, API ChessMasterAI |
| Frontend (Timestamp Player) | 1 000€ | Player vidéo avec marqueurs |
| Tests & Documentation | 500€ | Tests unitaires, guides MCP |
| **Total Build** | **4 000€** | **(-50% vs estimation précédente, sans entraînement)** |

**OPEX (12 mois)** :

| Poste | Coût mensuel | Coût annuel |
|-------|--------------|-------------|
| Infrastructure (GPU Cloud léger) | 150€ | 1 800€ |
| Stockage Vidéo (S3) | 100€ | 1 200€ |
| API YouTube (quotas) | 50€ | 600€ |
| Monitoring & Maintenance | 100€ | 1 200€ |
| **Total OPEX** | **400€** | **4 800€** |

**Récapitulatif** :

| Scénario | Coût |
|----------|------|
| Build Vidéo Vision | **4 000€** |
| OPEX 12 mois | **4 800€** |
| **Total 1ère année** | **8 800€** |
| Build + 24 mois OPEX | **13 600€** |

### 6.5 Limites & Solutions

| Limite | Impact | Solution |
|--------|--------|---------|
| Détection échiquier sensible | 🔥🔥 Fort | Calibration préalable, fallback manuel |
| Précision modèle pré-entraîné | 🔥 Moyen | Validation sur dataset échecs, fallback humain |
| Frames par seconde (coût) | 🔥 Moyen | Analyse sélective (1 frame/2 sec) |
| Conditions lumière | 🔥 Faible | Prétraitement images (normalisation) |
| Performance (GPU) | 🔥 Moyen | Redimensionnement frames, parallélisation |
| Stockage (volume) | 🔥 Moyen | Compression, nettoyage régulier |
| Dépendance YouTube | 🔥 Moyen | Mirroring local, multiples sources |

### 6.6 Roadmap

**Phase 1 : POC (2 semaines)** ✅
- Pipeline basique : extraction frames (FFmpeg)
- Intégration modèle pré-entraîné HF (`dopaul/chess_piece_detection`)
- Conversion FEN basique (mapping détection → board 8x8)

**Phase 2 : Intégration MCP (1 mois)** 🔨
- Serveur MCP complet
- Intégration ChessMasterAI
- Player vidéo avec UI timestamps

**Phase 3 : Scale & Optimisation (continu)** 🔨
- Benchmark `dopaul` vs `NAKSTStudio/yolov8m`
- Compression vidéos intelligente
- Cache FEN predictions
- Analytics d'usage

---

## 7. Conclusion

Ce POC démontre la faisabilité d'un agent IA pour l'apprentissage des échecs. L'architecture LangGraph + RAG offre une base solide pour étendre les capacités (MCP, Computer Vision).

**Prochaines étapes :**
1. Validation POC avec utilisateurs réels
2. Intégration MCP pour modularité
3. Développement module Computer Vision

---

*Document généré dans le cadre du Projet P13 - Formation Agents IA*
