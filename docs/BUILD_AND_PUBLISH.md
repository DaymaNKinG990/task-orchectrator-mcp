# Building and Publishing MCP Server

This guide describes the process of building and publishing the MCP server `@daymanking990/task-orchectrator-mcp` as an npm package for use in other projects.

## Prerequisites

### 1. Installing tools

```bash
# Install Node.js and npm (if not already installed)
# Download from https://nodejs.org/

# Install uv for Python dependencies
pip install uv

# Check versions
node --version
npm --version
uv --version
```

### 2. Setting up npm account

1. Create an account on [npmjs.com](https://www.npmjs.com/signup)
2. Login to npm in terminal:
```bash
npm login
```
3. Create organization (optional):
```bash
npm org create daymanking990
```

## Local build and testing

### 1. Project verification

```bash
# Check Python syntax
python -m py_compile src/task_orchectrator_mcp/server.py

# Check dependencies
uv sync

# Test server
uv run python -m task_orchectrator_mcp.server
```

### 2. Test npm package locally

```bash
# Create local package
npm pack

# Install package globally for testing
npm install -g ./daymanking990-task-orchectrator-mcp-0.3.0.tgz

# Test command
task-orchectrator-mcp

# Remove test installation
npm uninstall -g @daymanking990/task-orchectrator-mcp
```

### 3. Test via npx

```bash
# Run via npx
npx ./daymanking990-task-orchectrator-mcp-0.3.0.tgz
```

## Publishing to npm

### 1. Prepare for publishing

```bash
# Check package.json
npm run test

# Check package contents
npm pack --dry-run

# Check metadata
npm view @daymanking990/task-orchectrator-mcp
```

### 2. Publishing

```bash
# Publish to npm
npm publish

# For publishing to organization (if using scope)
npm publish --access public
```

### 3. Verify publishing

```bash
# Check on npmjs.com
# https://www.npmjs.com/package/@daymanking990/task-orchectrator-mcp

# Install from npm
npm install -g @daymanking990/task-orchectrator-mcp

# Test installed package
task-orchectrator-mcp
```

## Using in other projects

### 1. Install as dependency

```bash
# In new project
npm install @daymanking990/task-orchectrator-mcp
```

### 2. Use in MCP clients

#### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "task-orchectrator": {
      "command": "npx",
      "args": ["@daymanking990/task-orchectrator-mcp"],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key",
        "TRELLO_TOKEN": "your_trello_token",
        "TRELLO_WORKING_BOARD_ID": "your_board_id"
      }
    }
  }
}
```

#### Other MCP clients

```bash
# Direct run
npx @daymanking990/task-orchectrator-mcp

# With environment variables
TRELLO_API_KEY=your_key TRELLO_TOKEN=your_token npx @daymanking990/task-orchectrator-mcp
```

## Automation with GitHub Actions

### 1. Create workflow

Create `.github/workflows/publish-npm.yml`:

```yaml
name: Publish to npm

on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: ["18", "20"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - name: Install uv
      run: |
        pip install uv
        uv --version
    
    - name: Install dependencies
      run: uv sync
    
    - name: Check syntax
      run: python -m py_compile src/task_orchectrator_mcp/server.py
    
    - name: Test import
      run: uv run python -c "import task_orchectrator_mcp; print('✅ Import successful')"

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        registry-url: 'https://registry.npmjs.org'
    
    - name: Install uv
      run: |
        pip install uv
        uv --version
    
    - name: Install dependencies
      run: uv sync
    
    - name: Publish to npm
      run: npm publish --access public
      env:
        NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### 2. Configure secrets

In GitHub repository settings, add:
- `NPM_TOKEN` - npm access token (create at https://www.npmjs.com/settings/tokens)

## Versioning

### 1. Update version

```bash
# In package.json change version
"version": "0.3.1"  # or next version

# Also update version in pyproject.toml and __init__.py
```

### 2. Create release

```bash
# Create tag
git tag v0.3.1
git push origin v0.3.1

# Or create new release through GitHub UI
```

## Troubleshooting

### Build errors

```bash
# Check Node.js and npm
node --version
npm --version

# Clear npm cache
npm cache clean --force

# Check package.json
npm run test
```

### Publishing errors

```bash
# Check authorization
npm whoami

# Check package before publishing
npm pack --dry-run

# Check metadata
npm view @daymanking990/task-orchectrator-mcp
```

### Installation issues

```bash
# Force reinstall
npm install -g @daymanking990/task-orchectrator-mcp --force

# Check installed packages
npm list -g | grep task-orchectrator
```

## Useful commands

```bash
# View package information
npm view @daymanking990/task-orchectrator-mcp

# Check compatibility
npx @daymanking990/task-orchectrator-mcp --help

# Run with debugging
DEBUG=* npx @daymanking990/task-orchectrator-mcp
```

## Next steps

1. **Documentation**: Create documentation on npmjs.com or GitHub Pages
2. **Tests**: Add unit tests to improve quality
3. **CI/CD**: Set up automatic tests and code quality checks
4. **Monitoring**: Set up monitoring for downloads and package usage
5. **Updates**: Set up automatic dependency updates 