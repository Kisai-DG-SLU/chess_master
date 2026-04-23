# Note d'Analyse - Système Vidéo ChessMasterAI

## 🎯 Objectif

Concevoir un système avancé d'analyse vidéo pour enrichir les recommandations de l'agent IA ChessMasterAI. Le système permet de :
- Stocker des vidéos pertinentes (YouTube, uploads)
- Analyser chaque vidéo frame par frame
- Détecter l'échiquier et convertir en notation FEN
- Rechercher par position exacte dans le catalogue
- Servir le lien avec timestamp précis via MCP

---

## ✅ Bénéfices attendus

| Bénéfice | Description | Impact |
|-----------|-------------|--------|
| **Précision** | Timestamp exact pour le coup demandé (pas de vidéo de 45 min pour 1 coup) | 🔥🔥 Fort |
| **Pertinence** | Recherche par position FEN exacte vs mots-clés textuels | 🔥🔥 Fort |
| **Expérience UX** | L'utilisateur arrive directement sur le coup qui l'intéresse | 🔥🔥 Fort |
| **Automatisation** | Pipeline automatisé : ingéstion → analyse → indexation | 🔥 Moyen |
| **Évolutivité** | Intégration MCP pour modularité maximale | 🔥 Moyen |
| **Valeur ajoutée** | Différenciation compétitive face aux outils existants | 🔥🔥 Fort |

### 🎬 Exemple d'utilisation :
1. Utilisateur joue un coup en e4
2. Agent détecte position Ruy Lopez
3. Recherche dans catalogue vidéo : "Ruy Lopez, coup 5... a6"
4. Retourne : `https://youtube.com/watch?v=XXX&t=342s` (timestamp exact au coup demandé)

---

## ⚠️ Limites techniques et solutions

| Limite | Description | Impact | Solution提案 |
|--------|-------------|--------|----------------|
| **Détection échiquier** | Nécessite YOLO/OpenCV, sensible à l'angle de caméra | 🔥🔥 Fort | Calibration préalable, fallback manuel |
| **Reconnaissance pièces** | Erreurs de lecture (ex: Cvalier vs Fou) | 🔥 Moyen | Modèle CNN entraîné spécialement, validation humaine |
| **Frames par seconde** | Analyser toutes les frames = coûteux (vidéo 1h = 216k frames) | 🔥 Moyen | Analyse sélective (1 frame/2 sec), détection mouvements |
| **Lumière/Ombres** | Conditions d'éclairage affectent la précision | 🔥 Faible | Prétraitement images (normalisation) |
| **Multiples caméras** | Plusieurs angles dans une vidéo = confusion | 🔥 Moyen | Tracking de l'échiquier principal, masquage |
| **Performance** | Analyse vidéo 1080p = lourd en CPU/GPU | 🔥🔥 Fort | Redimensionnement, parallélisation, GPU cloud |
| **Stockage** | Vidéos HD = volume énorme (10 Go/heure) | 🔥 Moyen | Compression, stockage cloud (S3), nettoyage régulier |
| **Dépendance YouTube** | API YouTube limite les requêtes, vidéos supprimées | 🔥 Moyen | Mirroring local, multiples sources, playlists privées |

---

## 🏗️ Architecture MCP (Model Context Protocol)

Le système s'interfacera via MCP pour une modularité totale :

```
┌──────────────────────────────────────────────────────────────┐
│                    Client MCP (ChessMasterAI)                │
└──────────────────────────────┬─────────────────────────────┘
                               │ MCP
         ┌───────────────────────┼───────────────────────┐
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Video MCP     │  │  Chess Vision  │  │  Search MCP   │
│  Server        │  │  MCP Server   │  │  Server        │
│                │  │                │  │                │
│ Ingestion      │  │ FEN Extraction│  │ FEN Search     │
│ Stockage       │  │ Board Detection│  │ Timestamp     │
│ YouTube API    │  │ Piece Detect.  │  │ Ranking       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Protocol MCP :
- **Requête** : `find_video(fen: string, move_number: int)`
- **Réponse** : `{ url: string, timestamp: int, title: string }`
- **Transport** : Stdio, HTTP, WebSocket

---

## 💰 Étude de faisabilité (Estimation coûts)

### 🛠️ Développement (Build)

| Poste | Coût estimé | Détails |
|-------|-------------|---------|
| **Développement Vidéo Pipeline** | 2 000€ | Ingestion YouTube, extraction frames, stockage |
| **Modèle Vision (YOLO + CNN)** | 3 000€ | Entraînement, validation, optimisations |
| **Serveur MCP & Intégration** | 1 500€ | Dev MCP server, API ChessMasterAI |
| **Frontend (Timestamp Player)** | 1 000€ | Player vidéo avec markers temporels |
| **Tests & Documentation** | 500€ | Tests unitaires, doc MCP, guides |
| **Total Build** | **8 000€** | |

### 🔄 OPEX (12 mois)

| Poste | Coût mensuel | Coût annuel |
|-------|--------------|-------------|
| **Infrastructure (GPU Cloud)** | 300€ | 3 600€ |
| **Stockage Vidéo (S3)** | 100€ | 1 200€ |
| **API YouTube (quotas)** | 50€ | 600€ |
| **Monitoring & Maintenance** | 150€ | 1 800€ |
| **Total OPEX** | **600€** | **7 200€** |

### 📊 Récapitulatif

| Scénario | Coût |
|----------|------|
| Build Vidéo Vision | **8 000€** |
| OPEX 12 mois | **7 200€** |
| **Total 1ère année** | **15 200€** |
| Build + 24 mois OPEX | **22 400€** |

---

## 🛣 Roadmap de développement

### Phase 1 : POC (2 semaines)
- ✅ Pipeline basique : extraction frames (FFmpeg)
- ✅ Détection échiquier (OpenCV/Harris)
- ✅ Conversion FEN basique (sans CNN)

### Phase 2 : Modèle Avancé (1 mois)
- 🔨 Entraînement CNN (10k images annotées)
- 🔨 Optimisation précision pièces (>95%)
- 🔨 Gestion multi-angles

### Phase 3 : MCP & Production (1 mois)
- 🔨 Serveur MCP complet
- 🔨 Intégration ChessMasterAI
- 🔨 Player vidéo avec UI timestamps

### Phase 4 : Scale & Optimisation (continu)
- 🔨 Compression vidéos intelligente
- 🔨 Cache FEN predictions
- 🔨 Analytics de usage

---

## 🎯 Conclusion

Ce système de **Computer Vision pour vidéos d'échecs** représente une innovation majeure pour ChessMasterAI :

✅ **Valeur utilisateur** : Accès direct au coup cherché  
✅ **Innovation technique** : Vision + MCP + Chess  
✅ **Différenciation** : Aucun concurrent direct sur le marché  
✅ **Évolutivité** : Base pour d'autres sports/jeux  

**Investissement recommandé** : 15k€ pour l'année 1, ROI attendu sous 18 mois grâce à l'acquisition utilisateurs.

---

*Document conçu dans le cadre du P13 - Agent IA Échecs FFE*
