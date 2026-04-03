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

## 6. Perspectives - Computer Vision

### 6.1 Vision Future

Conception d'un système d'analyse vidéo :

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐
│  Video  │───▶│  Frame   │───▶│  FEN    │───▶│ Analyse │
│  Input  │    │ Extract  │    │ Extract │    │  Agent  │
└─────────┘    └──────────┘    └─────────┘    └─────────┘
```

### 6.2 Composants

1. **Capture vidéo** : API caméra / upload
2. **Détection échiquier** : YOLO / OpenCV
3. **Lecture pièces** : CNN classification
4. **Génération FEN** : Transformation coordinate
5. **Analyse** : Agent existant

---

## 7. Conclusion

Ce POC démontre la faisabilité d'un agent IA pour l'apprentissage des échecs. L'architecture LangGraph + RAG offre une base solide pour étendre les capacités (MCP, Computer Vision).

**Prochaines étapes :**
1. Validation POC avec utilisateurs réels
2. Intégration MCP pour modularité
3. Développement module Computer Vision

---

*Document généré dans le cadre du Projet P13 - Formation Agents IA*
