#!/usr/bin/env bash
# Streamlit runner with proper PYTHONPATH setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to project root
cd "$SCRIPT_DIR"

# Set PYTHONPATH to project root
export PYTHONPATH="$SCRIPT_DIR"

# Run streamlit
exec .venv/bin/streamlit run drivers/ui/streamlit/Home.py "$@"
