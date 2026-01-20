#!/bin/bash
set -e

# Usage: Executed INSIDE the container to run tests.
# 1. Install Test Dependencies
# We install globally inside the container (no venv needed)
if [ -f "tests/requirements.txt" ]; then
    echo "[INFO] Installing test dependencies..."
    pip install --no-cache-dir -r tests/requirements.txt
else
    echo "[ERROR] tests/requirements.txt not found!"
    exit 1
fi

# Run tests
echo "[INFO] Running Pytest..."
# -v: verbose
# -s: show stdout (print statements)
pytest -v -s