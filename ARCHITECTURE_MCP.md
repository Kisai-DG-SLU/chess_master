# Architecture MCP - Système Vidéo ChessMasterAI#

## 🎯 Objectif MCP (Model Context Protocol)

Permettre à l'agent ChessMasterAI d'interfacer avec le système de recherche vidéo de manière modulaire et standardisée.

---

## 🏗️ Architecture Globale

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client MCP (ChessMasterAI)                │
│              (Intégré dans agent/tools.py)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │ MCP (Stdio / HTTP / WebSocket)
         ┌──────────────────┴──────────────────┐
         │                                  │
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Video MCP    │  │ Vision MCP   │  │ Search MCP  │
│ Server      │  │ Server       │  │ Server      │
│             │  │              │  │             │
│ Ingestion   │  │ Détection   │  │ Recherche   │
│ Stockage    │  │ FEN Extraction│  │ Timestamp   │
│ YouTube API │  │ Board/CNN   │  │ Ranking    │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 📁 Serveurs MCP Détaillés

### 1️⃣ **Video MCP Server** (Gestion Vidéos)
- **Rôle** : Ingestion, stockage, métadonnées
- **Outils exposés** :
  - `ingest_video(url: string)` → `{ video_id, status }`
  - `get_video_info(video_id: string)` → `{ title, duration, fps }`
  - `extract_frames(video_id: string, interval: int)` → `{ frame_ids[] }`
  - `cleanup_old_videos(retention_days: int)` → `{ deleted_count }`

### 2️⃣ **Vision MCP Server** (Analyse Frames)
- **Rôle** : Détecter l'échiquier et extraire la position FEN
- **Outils exposés** :
  - `detect_board(frame_id: string)` → `{ has_board: bool, coords }`
  - `extract_fen(frame_id: string)` → `{ fen: string, confidence }`
  - `verify_position(fen: string, move_number: int)` → `{ is_valid: bool }`

### 3️⃣ **Search MCP Server** (Recherche Positionnelle)
- **Rôle** : Indexer et rechercher par position FEN exacte
- **Outils exposés** :
  - `index_video_position(video_id: string, fen: string, timestamp: int)` → `{ success }`
  - `search_by_fen(fen: string, move_context: string)` → `[{ video_id, timestamp, title, relevance }]`
  - `get_video_segment(video_id: string, start_ts: int, end_ts: int)` → `{ url_with_timestamp }`

---

## 🔄 Flux de Données (Pipeline Complet)

```
1. Ingestion YouTube
   ↳ Video MCP : ingest_video("https://youtube.com/watch?v=XXX")
   ↳ Stockage cloud (S3), métadonnées en DB

2. Extraction Frames
   ↳ Video MCP : extract_frames(video_id, interval=2)
   ↳ Génère 1 frame toutes les 2 secondes

3. Analyse Vision
   ↳ Vision MCP : extract_fen(frame_12345)
   ↳ Retourne : { fen: "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3", confidence: 0.95 }

4. Indexation
   ↳ Search MCP : index_video_position(video_id, fen, timestamp=342)
   ↳ Stockage dans base vectorielle (Milvus) + index FEN

5. Recherche (Utilisateur)
   ↳ Agent ChessMasterAI : "Joue e4, besoin vidéo Ruy Lopez"
   ↳ Search MCP : search_by_fen("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
   ↳ Retourne : [{ url: "https://youtube.com/watch?v=XXX&t=342s", title: "Ruy Lopez - Coup 5 expliqué" }]
```

---

## 🔌 Configuration Technique

### Transport MCP
- **Développement** : Stdio (standard in/out)
- **Production** : HTTP avec authentification JWT
- **WebSocket** : Pour updates temps réel (progression analyse)

### Format des Messages
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "extract_fen",
    "arguments": {
      "frame_id": "vid_123_frame_456"
    }
  },
  "id": 1
}
```

### Sécurité
- **Authentification** : API Keys par serveur MCP
- **Rate Limiting** : 100 req/min par client
- **Sandboxing** : Isolation des processus Vision (YOLO/CNN)

---

## 📊 Base de Données (Milvus + MongoDB)

```
┌─────────────────────┐     ┌─────────────────────┐
│     Milvus         │     │     MongoDB        │
│                    │     │                    │
│ Collections:       │     │ Collections:       │
│ - video_frames    │     │ - videos           │
│   (vectorielle)   │     │   (métadonnées)    │
│                    │     │ - positions        │
│ Champs:           │     │   (FEN + timestamps) │
│ - fen_embedding  │     │                    │
│ - timestamp      │     │ Champs:           │
│ - video_id      │     │ - url             │
│ - confidence    │     │ - title            │
└─────────────────────┘     │ - duration         │
                              └─────────────────────┘
```

---

## 🚀 Code d'Intégration (Exemple Agent)

```python
# agent/tools.py (extrait)
class ChessVideoSearchTool:
    def __init__(self, mcp_client):
        self.mcp = mcp_client  # Client MCP ChessMasterAI
    
    def search_video_by_position(self, fen: str, move_context: str = ""):
        """Recherche une vidéo par position FEN exacte"""
        try:
            result = self.mcp.call_tool(
                server="search",
                tool="search_by_fen",
                arguments={"fen": fen, "move_context": move_context}
            )
            return result["content"][0]["text"]  # URLs + timestamps
        except Exception as e:
            return f"Erreur recherche vidéo: {str(e)}"
```

---

## 📈 Monitoring & Métriques

| Métrique | Outil | Seuil Alerte |
|----------|------|--------------|
| **Disponibilité MCP** | Prometheus | < 99.9% |
| **Latence Recherche** | Grafana | > 500ms |
| **Précision FEN** | Custom | < 90% |
| **Couverture Vidéos** | Dashboard | < 80% |

---

## 🎬 Schéma de Déploiement

```
┌────────────────────────────────────────────────────┐
│              Docker Compose (Production)              │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Chess    │  │  Video  │  │  Vision │   │
│  │ Master  │  │  MCP    │  │  MCP    │   │
│  │  AI     │  │  Server │  │  Server │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│        │              │               │            │
│        ▼              ▼               ▼            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Search  │  │  Milvus  │  │  Redis  │   │
│  │  MCP    │  │  Vector  │  │  Cache  │   │
│  │  Server │  │  DB      │  │         │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
└────────────────────────────────────────────────────┘
```

---

## ✅ Avantages MCP pour ChessMasterAI

| Avantage | Description |
|----------|-------------|
| **Modularité** | Chaque serveur peut être développé indépendamment |
| **Réutilisabilité** | Serveurs MCP réutilisables par d'autres agents |
| **Scalabilité** | Scale horizontale par serveur |
| **Standardisation** | Compatible avec l'écosystème MCP (Claude, GPT) |
| **Maintenance** | Remplacement d'un serveur sans impacter les autres |

---

*Document conceptuel créé pour le P13 - Agent IA Échecs FFE*
