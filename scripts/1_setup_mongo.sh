#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

echo "--- Seeding MongoDB ---"
mongosh "$MONGODB_DATABASE_URL" --file "$PROJECT_ROOT/config/database/mongo/seed.js"

echo "--- Pulling MongoDB Prisma Schema ---"
cd "$PROJECT_ROOT/config/database/mongo"
python -m prisma db pull --force
python -m prisma generate