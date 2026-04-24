# Livrable 3 - Note détaillée

**Projet :** ChessMasterAI - Agent IA pour l'apprentissage des échecs (FFE)
**Auteur :** Damien Guesdon
**Date :** 04/2026

## Documents inclus

### 1. Note de cadrage (NOTE_CADRAGE.md)
Note détaillée de 8-10 pages couvrant :
- Architecture technique (POC et future architecture MCP)
- Stack technologique (LangGraph, FastAPI, Milvus, MongoDB, Angular, Stockfish)
- Étude de faisabilité avec chiffrage précis
- Coûts de développement (Build) : 7 000€
- Coûts opérationnels (OPEX) : 450€/mois
- Coût total 1ère année : 12 400€

### 2. Note bénéfices/limites système vidéo (NOTE_VISION.md)
Analyse du système avancé d'analyse vidéo :
- Bénéfices attendus (précision, pertinence, UX, automatisation)
- Limites techniques (détection échiquier, reconnaissance pièces, performance)
- Solutions proposées pour chaque limite
- Exemple d'utilisation concret

### 3. Architecture MCP (ARCHITECTURE_MCP.md)
Schéma d'architecture technique complète :
- Architecture globale Client MCP → Serveurs
- Serveurs MCP détaillés (Video, Vision, Search)
- Flux de données (Pipeline complet)
- Configuration technique (Transport, Sécurité)
- Base de données (Milvus + MongoDB)
- Code d'intégration exemple
- Monitoring & Métriques
- Schéma de déploiement Docker Compose

### 4. Roadmap de développement

| Phase | Durée | Livrable |
|-------|-------|----------|
| Phase 1 : POC | 2 semaines | Pipeline basique (FFmpeg, OpenCV) |
| Phase 2 : Modèle Avancé | 1 mois | CNN (10k images), précision >95% |
| Phase 3 : MCP & Production | 1 mois | Serveur MCP complet, UI timestamps |
| Phase 4 : Scale | Continu | Compression, cache, analytics |

### 5. Étude de faisabilité système vidéo

**Coûts Build :**
- Pipeline Vidéo : 2 000€
- Modèle Vision (YOLO+CNN) : 3 000€
- Serveur MCP & Intégration : 1 500€
- Frontend (Timestamp Player) : 1 000€
- Tests & Documentation : 500€
- **Total Build : 8 000€**

**Coûts OPEX (12 mois) :**
- Infrastructure (GPU Cloud) : 300€/mois
- Stockage Vidéo (S3) : 100€/mois
- API YouTube (quotas) : 50€/mois
- Monitoring & Maintenance : 150€/mois
- **Total OPEX : 600€/mois (7 200€/an)**

**Coût total 1ère année : 15 200€**

## Accès aux documents

Les documents complets sont disponibles dans le dépôt Git :
- `NOTE_CADRAGE.md`
- `NOTE_VISION.md`
- `ARCHITECTURE_MCP.md`
