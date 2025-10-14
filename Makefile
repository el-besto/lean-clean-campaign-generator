# -------- Project Settings --------
PYTHON := .venv/bin/python
COMPOSE := docker compose
WEAVIATE_HOST := 127.0.0.1
WEAVIATE_HTTP_PORT := 8080

.PHONY: help install test test-features clean demo cli ui up down clean-infra readiness open

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	python3.11 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:  ## Run all tests
	.venv/bin/pytest -v

test-features:  ## Run feature tests only
	.venv/bin/pytest tests/features/ -v -m acceptance

demo:  ## Run CLI demo
	cd "$(shell pwd)" && export PYTHONPATH=. && .venv/bin/python -m drivers.cli.commands demo

cli:  ## Run CLI (use: make cli ARGS="generate --help")
	cd "$(shell pwd)" && export PYTHONPATH=. && .venv/bin/python -m drivers.cli.commands $(ARGS)

ui:  ## Run Streamlit UI
	./run_streamlit.sh

clean:  ## Clean generated files
	rm -rf .pytest_cache
	rm -rf out/assets/*
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# -------- Docker Services --------
up:  ## Start Weaviate + MinIO services
	$(COMPOSE) up -d
	@echo ""
	@echo "Services starting..."
	@echo "  Weaviate:      http://$(WEAVIATE_HOST):$(WEAVIATE_HTTP_PORT)"
	@echo "  MinIO Console: http://127.0.0.1:9001 (login: minio/minio123)"
	@echo ""
	@echo "Run 'make readiness' to check Weaviate status"

down:  ## Stop services
	$(COMPOSE) down

clean-infra:  ## Stop services and remove volumes (fresh start)
	$(COMPOSE) down -v
	@echo "All volumes removed. Fresh start next time."

readiness:  ## Check Weaviate readiness
	@echo "Checking Weaviate readiness..."
	@curl -s -o /dev/null -w "%{http_code}" http://$(WEAVIATE_HOST):$(WEAVIATE_HTTP_PORT)/v1/.well-known/ready | grep -q "200" && echo "✅ Weaviate ready (HTTP 200)" || echo "❌ Weaviate not ready"

open:  ## Open service UIs in browser
	@open "http://$(WEAVIATE_HOST):$(WEAVIATE_HTTP_PORT)" || true
	@open "http://127.0.0.1:9001" || true

.DEFAULT_GOAL := help
