# Justification des Coûts - ChessMasterAI

## Build (7 000€)

| Poste | Coût | Justification |
|-------|------|---------------|
| Développement backend | 3 000€ | 20 jours × 150€/jour (tarif développeur junior France) |
| Intégration RAG | 1 500€ | 10 jours × 150€/jour (Milvus + embeddings) |
| Frontend Angular | 1 500€ | 10 jours × 150€/jour (ngx-chessboard + UI) |
| Docker & DevOps | 500€ | 3 jours × 150€/jour (docker-compose, volumes) |
| Tests & Documentation | 500€ | 3 jours × 150€/jour (tests API, README, specs) |
| **Total** | **7 000€** | |

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

| Poste | Coût | Justification |
|-------|------|---------------|
| Pipeline Vidéo | 2 000€ | FFmpeg, stockage S3, métadonnées |
| Modèle Vision (YOLO+CNN) | 3 000€ | Entraînement sur 10k images annotées |
| Serveur MCP | 1 500€ | Dev serveur + API ChessMasterAI |
| Frontend Timestamp Player | 1 000€ | Player vidéo avec marqueurs temporels |
| Tests & Documentation | 500€ | Tests unitaires, guides MCP |
| Infrastructure GPU | 3 600€/an | Instance GPU cloud (AWS p3.large ≈ 300€/mois) |
| Stockage Vidéo S3 | 1 200€/an | 100€/mois pour 500Go stockage + transfert |
| API YouTube | 600€/an | Quota API dépassé (50€/mois au-delà des quotas gratuits) |
| Monitoring | 1 800€/an | 150€/mois (inférence GPU + supervision) |
| **Total Vision Build** | **8 000€** | |
| **Total Vision OPEX** | **7 200€/an** | |
| **Total Vision 1ère année** | **15 200€** | |

---

## Notes

- Les coûts sont des **estimations** pour l'étude de faisabilité
- Non contractuels, sujets à variation selon le fournisseur
- Tarifs basés sur le marché français (2026)
- OVH Cloud, Scaleway, AWS Europe (Frankfurt)
- GPU : NVIDIA T4 ou V100 pour inférence vision

---

*Document généré pour la soutenance P13 - Damien Guesdon*
