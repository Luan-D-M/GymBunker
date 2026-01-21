#!/bin/bash
set -e

# Usage: Executed INSIDE the container to run tests. (no venv needed)
# Install Test Dependencies
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