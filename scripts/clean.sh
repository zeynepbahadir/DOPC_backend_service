#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting cleanup...${NC}"

# Remove Python cache files
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete
find . -type f -name ".pytest_cache" -delete
find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Remove virtual environment
echo "Removing virtual environment..."
rm -rf ./.venv/

echo -e "${GREEN}Cleanup completed!${NC}"
