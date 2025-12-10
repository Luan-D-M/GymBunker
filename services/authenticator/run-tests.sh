#!/bin/bash
#
# run-tests.sh
#
# Description:
#   Creates (if missing) and activates a Python virtual environment,
#   installs test dependencies and runs the test suite with pytest.
#
# Usage:
#   ./run-tests.sh           # set up venv + install deps + run tests
#   ./run-tests.sh clean     # also deletes the venv folder when tests are finished.
#
# Requirements:
#   Must be executed from ./services/authenticator (where ./auth_api.py and ./tests/ exist).
#
set -e
# --- Config ---
VENV_DIR="./venv"
REQ_FILE="./tests/requirements.txt"

# Check if the script has been executed from the correct path!
if [ ! -f "auth_api.py" ] || [ ! -d "tests" ]; then
  echo "[ERROR] This script must be executed from ./services/authenticator (where ./auth_api.py and ./tests/ exist) !!"
  exit 1
fi

echo "[INFO] Creating virtual environment at '$VENV_DIR'..."
python3 -m venv $VENV_DIR
source "venv/bin/activate"
echo "[INFO] Installing Python dependencies..."
pip install -r "$REQ_FILE"
echo "[INFO] Running tests..."
pytest -v

# --- Clean option ---
if [ "$1" == "clean" ]; then
  echo "[INFO] Removing virtual environment at '$VENV_DIR'..."
  rm -rf "$VENV_DIR"
  echo "[INFO] Clean complete."
  exit 0
fi