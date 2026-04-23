# Note de Conception - Système d'Analyse Vidéo Automatique

## ChessMasterAI - Extension d'Analyse Vidéo

**Date :** Avril 2026  
**Projet :** P13 - ChessMasterAI pour la FFE  
**Version :** 1.0

---

## 1. Contexte et Objectifs

### 1.1 Problématique

Les utilisateurs de ChessMasterAI souhaitent pouvoir analyser leurs propres parties. currently, le système analyse des positions statiques via FEN, mais ne permet pas l'analyse de vidéos de parties jouées.

### 1.2 Objectif du Système

Développer un système automatique qui :
- Détecte un échiquier dans une vidéo (photo ou vidéo)
- Identifie les coups joués
- Génère une analyse automatique des erreurs et opportunités
- Propose des ressources vidéo pour s'améliorer

---

## 2. Architecture Technique avec MCP

### 2.1 Vue d'Ensemble

```
[Vidéo Source] → [Détection Échiquier] → [Tracking Pièces] → [Génération FEN]
                                                                  ↓
                                        [Analyse ChessMasterAI] ← [Comparaison]
                                                                  ↓
                                                        [Rapport d'Analyse]
```

### 2.2 Architecture MCP (Model Context Protocol)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client (Frontend)                        │
│                    Application Angular                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MCP Server (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Video Ingest │  │Chess Analyzer│  │  YouTube Search      │  │
│  │   Service    │  │    Agent     │  │     Tool             │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │              │
│  ┌──────┴─────────────────┴──────────────────────┴───────────┐ │
│  │                    Tool Registry (MCP)                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│  OpenCV/YOLO    │ │  Stockfish  │ │  Embeddings     │
│  (Vision)       │ │  (Analyse)  │ │  (RAG)          │
└─────────────────┘ └─────────────┘ └─────────────────┘
```

### 2.3 Composants MCP

#### Tool: `detect_board`
```python
@tool
def detect_board(image: Image) -> BoardDetectionResult:
    """Détecte et extrait l'échiquier d'une image ou frame vidéo."""
    # Utilise YOLO ou OpenCV
    # Retourne les coordonnées, perspective, et validation
```

#### Tool: `track_pieces`
```python
@tool
def track_pieces(video_frames: list[Frame]) -> PieceMovement:
    """Trace le mouvement des pièces entre frames."""
    # Suit les pièces et génère la séquence de coups
```

#### Tool: `generate_fen_sequence`
```python
@tool
def generate_fen_sequence(movements: PieceMovement) -> list[str]:
    """Génère la séquence de positions FEN."""
    # Convertit les mouvements en positions FEN
```

#### Tool: `analyze_game`
```python
@tool
def analyze_game(fen_sequence: list[str]) -> GameAnalysis:
    """Analyse complète de la partie."""
    # Appelle Stockfish pour chaque position
    # Identifie les erreurs et opportunités
```

---

## 3. Technologies Utilisées

### 3.1 Détection d'Échiquier

| Technologie | Avantages | Inconvénients |
|-------------|-----------|---------------|
| **YOLO v8** | Rapide, précis, détection temps réel | Requiert entraînement |
| **OpenCV** | Gratuit, bien documenté | Sensible aux rotations |
| **Chessboard.js** (web) | Facile à intégrer | Limité aux boards standard |

**Recommandation :** YOLO v8 avec modèle pré-entraîné sur échiquiers.

### 3.2 Tracking des Pièces

- **DeepSort** : Suivi multi-objets performant
- **Optical Flow** : Alternative légère pour vidéos de bonne qualité

### 3.3 Comparaison avec Base de Données

- **pymilvus** : Recherche vectorielle pour similaires
- **chess library** : Validation des coups et positions

---

## 4. Implémentation

### 4.1 Flux de Traitement

```python
async def process_video(video_path: str) -> GameAnalysis:
    # 1. Extraction des frames
    frames = await extract_frames(video_path)
    
    # 2. Détection de l'échiquier
    board = await detect_board(frames[0])
    
    # 3. Tracking des pièces
    movements = await track_pieces(frames, board)
    
    # 4. Génération FEN
    fen_sequence = await generate_fen_sequence(movements)
    
    # 5. Analyse avec agent existant
    analysis = await chess_agent.analyze_sequence(fen_sequence)
    
    # 6. Recherche vidéo éducative
    videos = await youtube_search(analysis.mistakes)
    
    return GameAnalysis(
        moves=fen_sequence,
        analysis=analysis,
        videos=videos,
        mistakes=list(analysis.errors),
        opportunities=list(analysis.opportunities)
    )
```

### 4.2 API Endpoints

```python
@app.post("/api/v1/analyze-video")
async def analyze_video(file: UploadFile):
    """Analyse une vidéo de partie d'échecs."""
    result = await process_video(file)
    return result

@app.get("/api/v1/analyze-video/{job_id}")
async def get_analysis_status(job_id: str):
    """Retourne le statut du traitement."""
    return {"status": "processing" | "completed" | "error"}
```

---

## 5. Estimations de Coûts

### 5.1 Coûts de Build

| Élément | Coût Estimé |
|---------|-------------|
| Développement (40h × 80€) | 3 200 € |
| Entraînement modèle YOLO | 500 € |
| Infrastructure de test | 200 € |
| **Total Build** | **3 900 €** |

### 5.2 Coûts Opérationnels (mensuels)

| Service | Estimation |
|---------|------------|
| Stockage vidéo (100Go) | 15 €/mois |
| GPU processing (AWS g4dn) | 150 €/mois |
| API YouTube (quota) | 0 € (limité) |
| Milvus Cloud | 50 €/mois |
| **Total OPEX** | **215 €/mois** |

### 5.3 Coût par Analyse

- Vidéo 5 min (300 frames) : ~0,15 € (GPU)
- Image unique : ~0,01 €

---

## 6. Bénéfices et Limitations

### 6.1 Bénéfices

1. **Analyse automatisée** : Plus besoin de saisie manuelle des coups
2. **Feedback instantané** : Identification immédiate des erreurs
3. **Apprentissage personnalisé** : Vidéos adaptées aux faiblesses détectées
4. **Accessibilité** : Permet aux klub de analyser leurs parties simplement

### 6.2 Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Qualité vidéo | Mauvaise luminosité → échecs | Guide utilisateur |
| Angles caméra | Perspective non standard | Modèle robuste requis |
| Temps de processing | 5 min vidéo → 30s | Async processing |
| Couverture pièces | Pieces cachées → trous | Validation humaine |

---

## 7. Risques et Alternatives

### 7.1 Risques Techniques

1. **Faux positifs détection** : Board détecté mais incorrect
   - Mitigation : Validation croisée avec détection de pièces

2. **Imprécision tracking** : Pièces confondues
   - Mitigation : Utiliser couleur distinctive

3. **Performance** : Temps de traitement trop long
   - Mitigation : Traitement asynchrone avec notifications

### 7.2 Alternatives

| Alternative | Complexité | Coût |
|-------------|------------|------|
| **Saisie manuelle + analyse** | Faible | 0 € |
| **API externe (Chess.com)** | Moyenne | 50 €/mois |
| **Solution proposée (MCP)** | Élevée | 215 €/mois |

### 7.3 Recommandation

**Implémenter progressivement :**
1. Phase 1 : Upload manuel de PGN + analyse
2. Phase 2 : Extraction automatique d'image unique
3. Phase 3 : Analyse vidéo complète

---

## 8. Conclusion

Le système d'analyse vidéo représente une valeur ajoutée significative pour les utilisateurs de ChessMasterAI. L'architecture MCP proposée permet une intégration propre avec les services existants (Stockfish, YouTube, RAG).

L'investissement initial de ~4 000 € et un coût opérationnel de ~215 €/mois permettent de proposer un service différenciant pour la FFE.

---

## Annexe : Plan de Développement

| Phase | Durée | Livrable |
|-------|-------|----------|
| Phase 1 | 2 semaines | Upload PGN + analyse |
| Phase 2 | 3 semaines | Extraction image → FEN |
| Phase 3 | 4 semaines | Analyse vidéo complète |
| Phase 4 | 2 semaines | Tests et documentation |

**Total :** 11 semaines

---

*Document généré pour la soutenance P13 - ChessMasterAI*