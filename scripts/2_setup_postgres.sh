#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

echo "--- Seeding PostgreSQL ---"
cd "$PROJECT_ROOT/config/database/postgres"

python -m prisma db execute --file seed.sql --schema prisma/schema.prisma

echo "--- Pulling PostgreSQL Prisma Schema ---"
python -m prisma db pull --force
python -m prisma generate
