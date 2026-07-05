#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "--- Running MongoDB Python Loader ---"
cd "$PROJECT_ROOT"

pipenv run python scripts/load_mongodb.py