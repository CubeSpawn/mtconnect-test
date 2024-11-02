#!/bin/bash
# Setup script for development environment

# Create Python virtual environment if it doesn't exist
if [ ! -d "/workspace/venv" ]; then
    python3 -m venv /workspace/venv
fi

# Activate virtual environment
source /workspace/venv/bin/activate

# Install development dependencies
pip install -r /workspace/requirements.txt

echo "Development environment setup complete!"