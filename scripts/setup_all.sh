#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo " Starting Full Database Initialization"
echo "========================================"

bash "$SCRIPT_DIR/1_setup_mongo.sh"
bash "$SCRIPT_DIR/2_setup_postgres.sh"
bash "$SCRIPT_DIR/3_load_mongo.sh"
bash "$SCRIPT_DIR/4_load_postgres.sh"

echo "========================================"
echo " Setup Complete!"
echo "========================================"