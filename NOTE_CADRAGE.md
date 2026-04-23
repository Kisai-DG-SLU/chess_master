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

**Solution conceptuelle** :
- Stocker les vidéos pertinentes (YouTube API)
- Analyser chaque frame pour détecter l'échiquier
- Convertir en notation FEN via modèle de vision
- Indexer par position exacte avec timestamps
- Servir via MCP (Model Context Protocol)

**Bénéfices** :
- ✅ Précision : Timestamp exact pour le coup demandé
- ✅ Pertinence : Recherche par FEN vs mots-clés
- ✅ UX : Accès direct au coup qui intéresse
- ✅ Innovation : Aucun concurrent direct sur le marché

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
| **Détection échiquier** | YOLO v8 / OpenCV | Harris corner, perspective transform |
| **Lecture pièces** | CNN personnalisé | Entraînement sur 10k images |
| **Génération FEN** | Algorithme coords | Transformation 8x8 → notation |
| **Indexation** | Milvus | Embeddings FEN, recherche vectorielle |
| **Serveur MCP** | Node.js / Python | Stdio, HTTP, WebSocket |

### 6.4 Étude de Faisabilité (Coût)

**Build (Développement)** :

| Poste | Coût estimé | Détails |
|-------|-------------|---------|
| Pipeline Vidéo | 2 000€ | FFmpeg, stockage S3, métadonnées |
| Modèle Vision (YOLO+CNN) | 3 000€ | Entraînement, validation, optim |
| Serveur MCP & Intégration | 1 500€ | Dev serveur, API ChessMasterAI |
| Frontend (Timestamp Player) | 1 000€ | Player vidéo avec marqueurs |
| Tests & Documentation | 500€ | Tests unitaires, guides MCP |
| **Total Build** | **8 000€** | |

**OPEX (12 mois)** :

| Poste | Coût mensuel | Coût annuel |
|-------|--------------|-------------|
| Infrastructure (GPU Cloud) | 300€ | 3 600€ |
| Stockage Vidéo (S3) | 100€ | 1 200€ |
| API YouTube (quotas) | 50€ | 600€ |
| Monitoring & Maintenance | 150€ | 1 800€ |
| **Total OPEX** | **600€** | **7 200€** |

**Récapitulatif** :

| Scénario | Coût |
|----------|------|
| Build Vidéo Vision | 8 000€ |
| OPEX 12 mois | 7 200€ |
| **Total 1ère année** | **15 200€** |
| Build + 24 mois OPEX | **22 400€** |

### 6.5 Limites & Solutions

| Limite | Impact | Solution |
|--------|--------|---------|
| Détection échiquier sensible | 🔥🔥 Fort | Calibration préalable, fallback manuel |
| Erreurs lecture pièces | 🔥 Moyen | CNN spécialisé, validation humaine |
| Frames par seconde (coût) | 🔥 Moyen | Analyse sélective, détection mouvements |
| Conditions lumière | 🔥 Faible | Prétraitement images (normalisation) |
| Multiples caméras | 🔥 Moyen | Tracking échiquier principal, masquage |
| Performance (GPU) | 🔥🔥 Fort | Parallélisation, GPU cloud |
| Stockage (volume) | 🔥 Moyen | Compression, nettoyage régulier |
| Dépendance YouTube | 🔥 Moyen | Mirroring local, multiples sources |

### 6.6 Roadmap

**Phase 1 : POC (2 semaines)** ✅
- Pipeline basique : extraction frames (FFmpeg)
- Détection échiquier (OpenCV/Harris)
- Conversion FEN basique (sans CNN)

**Phase 2 : Modèle Avancé (1 mois)** 🔨
- Entraînement CNN (10k images annotées)
- Précision pièces >95%
- Gestion multi-angles

**Phase 3 : MCP & Production (1 mois)** 🔨
- Serveur MCP complet
- Intégration ChessMasterAI
- Player vidéo avec UI timestamps

**Phase 4 : Scale & Optimisation (continu)** 🔨
- Compression vidéos intelligente
- Cache FEN predictions
- Analytics de usage

---

## 7. Conclusion

Ce POC démontre la faisabilité d'un agent IA pour l'apprentissage des échecs. L'architecture LangGraph + RAG offre une base solide pour étendre les capacités (MCP, Computer Vision).

**Prochaines étapes :**
1. Validation POC avec utilisateurs réels
2. Intégration MCP pour modularité
3. Développement module Computer Vision

---

*Document généré dans le cadre du Projet P13 - Formation Agents IA*
