#!/usr/bin/env bash

# Get the absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Direct to root path
PROJECT_ROOT="$SCRIPT_DIR/../"
cd "$PROJECT_ROOT"

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Print current directory for test purposes
echo "Current working directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"

# Execution
exec python -m training_box.env_service --env appworld --portal 0.0.0.0 --port 80