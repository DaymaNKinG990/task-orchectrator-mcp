# Quick MCP Server Publishing

## Prerequisites

1. **npm account**: Create at [npmjs.com](https://www.npmjs.com/signup)
2. **npm login**: `npm login`
3. **uv**: `pip install uv`

## Quick publishing

### 1. Update version

Update version in three files:
- `package.json`: `"version": "0.3.1"`
- `pyproject.toml`: `version = "0.3.1"`
- `src/task_orchectrator_mcp/__init__.py`: `__version__ = "0.3.1"`

### 2. Testing

```bash
# Create package
npm pack

# Test locally
npm install -g ./daymanking990-task-orchectrator-mcp-0.3.1.tgz
task-orchectrator-mcp

# Remove test installation
npm uninstall -g @daymanking990/task-orchectrator-mcp
```

### 3. Publishing

```bash
# Publish to npm
npm publish --access public
```

### 4. Verification

```bash
# Install from npm
npm install -g @daymanking990/task-orchectrator-mcp

# Test
task-orchectrator-mcp
```

## Usage in mcp.json

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

## Automatic publishing

Create a GitHub release - package will automatically publish to npm. 