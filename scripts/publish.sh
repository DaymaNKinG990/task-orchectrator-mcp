#!/bin/bash

# Script for building and publishing task-orchectrator-mcp package
# Usage: ./scripts/publish.sh [test|prod]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Get version from pyproject.toml
VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
print_status "Building version: $VERSION"

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
print_status "Installing build dependencies..."
uv add build twine --dev

# Check syntax
print_status "Checking syntax..."
python -m py_compile src/task_orchectrator_mcp/server.py

# Sync dependencies
print_status "Syncing dependencies..."
uv sync

# Build package
print_status "Building package..."
uv run python -m build

# Check package
print_status "Checking package..."
uv run python -m twine check dist/*

# Test local installation
print_status "Testing local installation..."
uv run pip install dist/*.whl --force-reinstall
uv run python -c "import task_orchectrator_mcp; print('✅ Package installed successfully')"

# Determine target
TARGET=${1:-test}

if [ "$TARGET" = "test" ]; then
    print_status "Publishing to TestPyPI..."
    uv run python -m twine upload --repository testpypi dist/*
    print_status "✅ Published to TestPyPI successfully!"
    print_warning "To install from TestPyPI: pip install --index-url https://test.pypi.org/simple/ task-orchectrator-mcp"
    
elif [ "$TARGET" = "prod" ]; then
    print_warning "Are you sure you want to publish to PyPI? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Publishing to PyPI..."
        uv run python -m twine upload dist/*
        print_status "✅ Published to PyPI successfully!"
        print_status "Package is now available at: https://pypi.org/project/task-orchectrator-mcp/"
    else
        print_status "Publishing cancelled."
        exit 0
    fi
    
else
    print_error "Invalid target. Use 'test' or 'prod'"
    exit 1
fi

print_status "Build and publish completed successfully!" 