#!/usr/bin/env bash
# exit on error
set -o errexit

# Force Python version
python --version

# Install dependencies
pip install -r requirements-render.txt

# Test import
python -c "import fastapi; print('FastAPI imported successfully')"
