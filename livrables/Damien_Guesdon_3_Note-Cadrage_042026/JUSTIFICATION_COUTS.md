# Justification des Coûts - ChessMasterAI

## Build (7 000€)

| Poste | Coût | Jours/hommes | Justification |
|-------|------|--------------|---------------|
| Développement backend | 3 000€ | 20 jours | 20 jours × 150€/jour (tarif développeur junior France) |
| Intégration RAG | 1 500€ | 10 jours | 10 jours × 150€/jour (Milvus + embeddings) |
| Frontend Angular | 1 500€ | 10 jours | 10 jours × 150€/jour (ngx-chessboard + UI) |
| Docker & DevOps | 500€ | 3 jours | 3 jours × 150€/jour (docker-compose, volumes) |
| Tests & Documentation | 500€ | 3 jours | 3 jours × 150€/jour (tests API, README, specs) |
| **Total** | **7 000€** | **46 jours** | |

**Base tarifaire** : 150€/jour HT = tarif moyen d'un développeur junior en France (stage/alternance facturé).

---

## OPEX (12 mois)

| Poste | Coût annuel | Justification |
|-------|-------------|---------------|
| Infrastructure cloud | 1 800€ | 1 VM + DB ≈ 150€/mois (OVH Cloud / Scaleway) |
| Monitoring | 1 200€ | 100€/mois (supervision, logs, alertes) |
| **Total** | **3 000€** | |

**Infrastructure** :
- 1 VM 2vCPU/4Go RAM ≈ 60€/mois
- Stockage SSD 50Go ≈ 20€/mois
- Bande passante ≈ 30€/mois
- DB managée (MongoDB Atlas free tier ou payant) ≈ 40€/mois

---

## Vision (Système Vidéo Avancé)

**Solution retenue** : Modèles pré-entraînés Hugging Face (pas d'entraînement custom)
- `dopaul/chess_piece_detection` : Fine-tuné sur dataset échecs
- `NAKSTStudio/yolov8m-chess-piece-detection` : YOLOv8 standard

| Poste | Coût | Jours/hommes | Justification |
|-------|------|--------------|---------------|
| Pipeline Vidéo | 1 500€ | 10 jours | FFmpeg, extraction frames, stockage S3, métadonnées |
| Intégration Modèle HF | 500€ | 3 jours | Chargement modèle pré-entraîné (pas d'entraînement) |
| Mapping FEN | 500€ | 3 jours | Algorithme détection → board 8x8 → notation FEN |
| Serveur MCP | 1 000€ | 7 jours | Dev serveur + API ChessMasterAI |
| Frontend Timestamp Player | 1 000€ | 7 jours | Player vidéo avec marqueurs temporels |
| Tests & Documentation | 500€ | 3 jours | Tests unitaires, guides MCP |
| **Total Vision Build** | **4 000€** | **33 jours** | **-50% vs estimation précédente (pas d'entraînement)** |
| **Total Vision OPEX** | **4 800€/an** | |
| **Total Vision 1ère année** | **8 800€** | |

---

## Notes

- Les coûts sont des **estimations** pour l'étude de faisabilité
- Non contractuels, sujets à variation selon le fournisseur
- Tarifs basés sur le marché français (2026)
- OVH Cloud, Scaleway, AWS Europe (Frankfurt)
- GPU : NVIDIA T4 ou V100 pour inférence vision

---

*Document généré pour la soutenance P13 - Damien Guesdon*
