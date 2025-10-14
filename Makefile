.PHONY: help install test test-features clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:  ## Run all tests
	.venv/bin/pytest -v

test-features:  ## Run feature tests only
	.venv/bin/pytest tests/features/ -v -m acceptance

clean:  ## Clean generated files
	rm -rf .pytest_cache
	rm -rf out/assets/*
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

.DEFAULT_GOAL := help
