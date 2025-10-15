# -------- Project Settings --------
PYTHON := .venv/bin/python
COMPOSE := docker compose
WEAVIATE_HOST := 127.0.0.1
WEAVIATE_HTTP_PORT := 8080

.DEFAULT_GOAL := help
.PHONY: help install test test-features clean demo cli ui present-all present-html present-pdf present-pptx present-notes seed up down clean-infra readiness open

# -------- Core Commands --------

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

seed:  ## Seed brand data to Weaviate (run after 'make up')
	cd "$(shell pwd)" && export PYTHONPATH=. && .venv/bin/python tools/seed_brand.py

open:  ## Open service UIs in browser
	@open "http://$(WEAVIATE_HOST):$(WEAVIATE_HTTP_PORT)" || true
	@open "http://127.0.0.1:9001" || true

# -------- Presentations --------

PRESENTATION_NAME := 'fde'
PRESENTATION_FILE = docs/presentation-$(PRESENTATION_NAME).md
MARP_FLAGS = --allow-local-files
MARP_CHECK = @command -v marp >/dev/null 2>&1 || { echo "Error: marp-cli not found. Install with: npm install -g @marp-team/marp-cli"; exit 1; }

define generate_presentation
	$(MARP_CHECK)
	marp $(PRESENTATION_FILE) --$(1) $(MARP_FLAGS) -o $(2)
	@echo "✅ $(3) generated: $(2)"
endef

present-html-build:  ## Generate HTML presentation
	$(call generate_presentation,html,docs/presentation-$(PRESENTATION_NAME).html,HTML presentation)

present-pdf-build:  ## Generate PDF presentation
	$(call generate_presentation,pdf,docs/presentation-$(PRESENTATION_NAME).pdf,PDF presentation)

present-pptx-build:  ## Generate PPTX presentation
	$(call generate_presentation,pptx,docs/presentation-$(PRESENTATION_NAME).pptx,PPTX presentation)

present-notes-build:  ## Generate notes
	$(call generate_presentation,notes,docs/presentation-$(PRESENTATION_NAME)-notes.txt,Notes)

present-html: present-html-build  ## Generate and open HTML presentation
	open docs/presentation-$(PRESENTATION_NAME).html

present-pdf: present-pdf-build  ## Generate and open PDF presentation
	open docs/presentation-$(PRESENTATION_NAME).pdf

present-pptx: present-pptx-build  ## Generate and open PPTX presentation
	open docs/presentation-$(PRESENTATION_NAME).pptx

present-notes: present-notes-build  ## Generate and open notes
	open docs/presentation-$(PRESENTATION_NAME)-notes.txt

present-all: present-html-build present-pdf-build present-pptx-build present-notes-build  ## Generate all presentations
