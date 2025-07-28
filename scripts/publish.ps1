# Script for building and publishing task-orchectrator-mcp package
# Usage: .\scripts\publish.ps1 [test|prod]

param(
    [Parameter(Position=0)]
    [ValidateSet("test", "prod")]
    [string]$Target = "test"
)

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Error "pyproject.toml not found. Please run this script from the project root."
    exit 1
}

# Get version from pyproject.toml
$Version = (Select-String '^version = ' pyproject.toml | ForEach-Object { $_.Line -replace 'version = "', '' -replace '"', '' }).Trim()
Write-Status "Building version: $Version"

# Clean previous builds
Write-Status "Cleaning previous builds..."
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.egg-info") { Remove-Item -Recurse -Force "*.egg-info" }

# Install build dependencies
Write-Status "Installing build dependencies..."
uv add build twine --dev

# Check syntax
Write-Status "Checking syntax..."
python -m py_compile src/task_orchectrator_mcp/server.py

# Sync dependencies
Write-Status "Syncing dependencies..."
uv sync

# Build package
Write-Status "Building package..."
uv run python -m build

# Check package
Write-Status "Checking package..."
uv run python -m twine check dist/*

# Test local installation
Write-Status "Testing local installation..."
uv run pip install dist/*.whl --force-reinstall
uv run python -c "import task_orchectrator_mcp; print('✅ Package installed successfully')"

# Determine target
if ($Target -eq "test") {
    Write-Status "Publishing to TestPyPI..."
    uv run python -m twine upload --repository testpypi dist/*
    Write-Status "✅ Published to TestPyPI successfully!"
    Write-Warning "To install from TestPyPI: pip install --index-url https://test.pypi.org/simple/ task-orchectrator-mcp"
    
} elseif ($Target -eq "prod") {
    Write-Warning "Are you sure you want to publish to PyPI? (y/N)"
    $response = Read-Host
    if ($response -match "^[yY](es)?$") {
        Write-Status "Publishing to PyPI..."
        uv run python -m twine upload dist/*
        Write-Status "✅ Published to PyPI successfully!"
        Write-Status "Package is now available at: https://pypi.org/project/task-orchectrator-mcp/"
    } else {
        Write-Status "Publishing cancelled."
        exit 0
    }
}

Write-Status "Build and publish completed successfully!" 