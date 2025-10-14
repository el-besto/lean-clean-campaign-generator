.PHONY: help install test test-features clean demo cli ui

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

.DEFAULT_GOAL := help
