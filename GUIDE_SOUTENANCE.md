# 📋 Guide de Soutenance P13 - ChessMasterAI

**Auteur :** Damien Guesdon  
**Date :** Avril 2026  
**Projet :** P13 - Formation Agents IA

---

## 🎯 CE QUE J'AI FAIT

### Le Projet en 1 Phrase

Un agent IA qui accompagne les jeunes joueurs d'échecs dans l'apprentissage des ouvertures, avec :
- Analyse de position via Stockfish
- Coups théoriques via Lichess
- Contexte via RAG sur Milvus
- Vidéos explicatives via YouTube API
- Interface Angular avec échiquier interactif

---

## 📖 COMMENT ÇA FONCTIONNE (Grandes Lignes)

### 1. L'Utilisateur
1. Place une position sur l'échiquier Angular
2. Clique "Analyser"
3. Voit les résultats

### 2. Le Backend (FastAPI)
1. Reçoit la position FEN
2. LangGraph orchestre 3 étapes :
   - **Analyse** : Stockfish évalue la position
   - **Théorie** : Lichess retourne les coups théoriques
   - **Recommandations** : Milvus trouve des ouvertures similaires
3. Retourne les résultats à l'interface

### 3. Les Services
- **Stockfish** : Moteur d'échecs (évaluation + meilleur coup)
- **Lichess API** : Base de données de coups théoriques
- **Milvus** : Base vectorielle pour recherche sémantique
- **MongoDB** : Stockage utilisateurs et parties
- **YouTube API** : Recherche de vidéos explicatives

---

## 📊 LES 7 ÉTAPES DE LA MISSION

### Étape 1 : Structure Projet ✅
- Git + README.md
- docker-compose.yml (FastAPI, Milvus, MongoDB, Angular)
- Structure dossiers claire

### Étape 2 : Endpoints Lichess/Stockfish ✅
- `GET /api/v1/moves?fen=...` → Coups théoriques
- `GET /api/v1/evaluate?fen=...` → Évaluation Stockfish

### Étape 3 : RAG avec Milvus ✅
- Base vectorielle avec 8 ouvertures
- `GET /vector-search?query=...` → Recherche sémantique
- Embeddings hash-based (fallback sans API key)

### Étape 4 : YouTube API ✅
- `GET /api/v1/videos?opening=...` → Recherche vidéos
- API officielle YouTube Data v3
- 5 vidéos retournées avec titre, URL, thumbnail

### Étape 5 : Interface Angular ✅
- ngx-chessboard intégré
- Boutons : Reset, Ruy Lopez, Sicilienne, Analyser
- Affichage des résultats + vidéos

### Étape 6 : Docker Compose ✅
- 5 services orchestrés
- Volumes persistants
- README avec instructions

### Étape 7 : Note de Conception ✅
- NOTE_CADRAGE.md : Note de cadrage + coûts
- NOTE_VISION.md : Bénéfices/limites système vidéo
- ARCHITECTURE_MCP.md : Schéma architecture MCP

---

## 💰 LES COÛTS (Notes de Cadrage)

### Build (Développement du POC)
| Poste | Coût |
|-------|------|
| Développement backend | 3 000€ |
| Intégration RAG | 1 500€ |
| Frontend Angular | 1 500€ |
| Docker & DevOps | 500€ |
| Tests & Documentation | 500€ |
| **Total Build** | **7 000€** |

### OPEX (12 mois)
| Poste | Coût annuel |
|-------|-------------|
| Infrastructure cloud | 1 800€ |
| Monitoring & maintenance | 1 200€ |
| **Total OPEX** | **3 000€** |

### Total 1ère année : **10 000€**

---

## 🔧 MCP (Model Context Protocol)

### C'est Quoi ?
Un standard pour connecter un LLM à des outils externes de manière modulaire.

### Pourquoi ?
Avec MCP, chaque outil est un "serveur" indépendant. Tu peux remplacer ou ajouter un outil sans casser le reste.

### Comment ?
```
LLM → MCP → [Stockfish MCP Server]
           → [Lichess MCP Server]
           → [Milvus MCP Server]
```

Le LLM ne sait pas comment fonctionne Stockfish, il appelle juste l'outil MCP Stockfish.

---

## 👁️ VISION (Système Vidéo Avancé)

### C'est Quoi ?
Une ÉTUDE CONCEPTUELLE (pas implémentée) pour analyser automatiquement des vidéos de parties d'échecs.

### Le Problème
Quand tu cherches "Ruy Lopez" sur YouTube, tu trouves des vidéos de 45 minutes. C'est pas pratique.

### La Solution Conceptuelle
1. Prendre une vidéo YouTube
2. Extraire chaque frame (image)
3. Détecter l'échiquier dans chaque frame
4. Convertir en notation FEN
5. Indexer dans Milvus avec le timestamp

### Résultat
Tu cherches "Ruy Lopez coup 5", tu obtiens le lien YouTube EXACT au timestamp du coup.

### Coûts de la Vision (Étude de Faisabilité)
| Poste | Coût |
|-------|------|
| Pipeline Vidéo | 2 000€ |
| Modèle Vision (YOLO+CNN) | 3 000€ |
| Serveur MCP & Intégration | 1 500€ |
| Frontend (Timestamp Player) | 1 000€ |
| Tests & Documentation | 500€ |
| **Total Build Vision** | **8 000€** |

**OPEX Vision** : 600€/mois (7 200€/an)

**Total 1ère année Vision** : **15 200€**

---

## 🎬 LA DÉMO (1 min)

1. **Montrer l'interface Angular**
   - Échiquier ngx-chessboard
   - Boutons : Reset, Ruy Lopez, Sicilienne

2. **Cliquer "Analyser"**
   - Appelle `/analyze`
   - Stockfish évalue la position
   - Lichess retourne les coups théoriques
   - Milvus trouve des ouvertures similaires

3. **Montrer les vidéos YouTube**
   - Appelle `/api/v1/videos`
   - 5 vidéos retournées
   - Titre, URL, thumbnail affichés

4. **Montrer MongoDB**
   - Section "Utilisateur" (créer un compte)
   - Bouton "Sauvegarder la partie"
   - Liste "Mes Parties"

5. **Dire**
   > "Tout est dans Docker Compose, 5 services orchestrés. Le POC est fonctionnel et prêt pour la soutenance."

---

## ✅ CONCLUSION

**Mission P13 respectée à 100%**

- ✅ 7 étapes conformes aux specs
- ✅ 3 livrables complets
- ✅ Démo Docker fonctionnelle
- ✅ Code complet (LangGraph, FastAPI, Milvus, MongoDB, Angular)
- ✅ Documentation complète (Cadrage, Vision, MCP)

**Prochaines étapes :**
- Validation POC avec utilisateurs réels
- Intégration MCP pour modularité
- Développement module Computer Vision

---

*Document généré pour la soutenance P13 - ChessMasterAI - Damien Guesdon*
