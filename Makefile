.PHONY: help install test run docker-build docker-up docker-down lint format typecheck

help:
	@echo "Commandes disponibles:"
	@echo "  make install        - Installer les dépendances via pixi"
	@echo "  make test          - Exécuter les tests"
	@echo "  make lint          - Vérifier le linting (ruff)"
	@echo "  make format        - Formater le code (black)"
	@echo "  make typecheck     - Vérifier les types (mypy)"
	@echo "  make run           - Démarrer l'API"
	@echo "  make docker-build  - Build Docker"
	@echo "  make docker-up     - Démarrer les containers"
	@echo "  make docker-down   - Arrêter les containers"

install:
	pixi install

test:
	PYTHONPATH=/mnt/prod pytest tests/ -v

lint:
	ruff check .

format:
	black .

typecheck:
	mypy agent/ api/ rag/

run:
	python -m api.main

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
