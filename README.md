# Task Orchestrator MCP Server

A sophisticated task orchestration system with role-based workflow management and Trello integration.

## Overview

The Task Orchestrator MCP server provides a comprehensive task management system with:

- **Role-based workflow management** with 5 distinct roles (Orchestrator, Architect, Coder, Analyst, DevOps)
- **Three-tier Trello integration** (MCP Server, Direct API, Local Storage)
- **Automatic task lifecycle management** with status tracking
- **Dependency management** between tasks
- **Persistent local storage** with JSON backup
- **Real-time status monitoring** and reporting

## Features

### Role System
- **Orchestrator**: Creates and assigns tasks, manages workflow
- **Architect**: Handles system design and architecture tasks
- **Coder**: Implements features and code changes
- **Analyst**: Performs analysis and research tasks
- **DevOps**: Manages deployment and infrastructure tasks

### Trello Integration Modes
1. **MCP Server Mode** (Priority 1): Uses MCP Trello server for integration
2. **Direct API Mode** (Priority 2): Direct Trello API integration
3. **Local Storage Mode** (Priority 3): Local JSON storage without Trello

### Task Management
- Automatic task creation with unique IDs
- Status tracking (TODO, IN_PROGRESS, REVIEW, DONE, BLOCKED)
- Dependency validation
- Role assignment and transitions
- Completion tracking with notes

## Components

### Resources

The server implements a task storage system with:
- Custom `task://` URI scheme for accessing individual tasks
- Each task resource has a name, description and JSON mimetype
- Automatic resource list updates when tasks change

### Tools

The server provides comprehensive task management tools:

#### Task Management
- `create_task`: Creates a new task (Orchestrator only)
- `assign_task`: Assigns task to a specific role (Orchestrator only)
- `complete_task`: Completes a task and returns control to Orchestrator
- `list_tasks`: Lists tasks with optional status filtering

#### Role Management
- `switch_role`: Switches to a different role (Orchestrator only)
- `return_to_orchestrator`: Returns control to Orchestrator
- `get_status`: Shows current system status and statistics

#### Trello Integration
- `sync_to_trello`: Syncs all tasks to Trello board
- `check_mcp_trello`: Checks MCP Trello server availability
- `export_tasks`: Exports tasks to local JSON files

## Configuration

### Environment Variables

For Direct API Trello integration:
```bash
TRELLO_API_KEY=your_api_key
TRELLO_TOKEN=your_token
TRELLO_WORKING_BOARD_ID=your_board_id
```

### MCP Server Configuration

#### Development/Unpublished Servers

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "task-orchectrator-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\xella\\PycharmProjects\\task-orchectrator-mcp",
        "run",
        "task-orchectrator-mcp"
      ],
      "env": {
        "TRELLO_API_KEY": "your_api_key",
        "TRELLO_TOKEN": "your_token",
        "TRELLO_WORKING_BOARD_ID": "your_board_id"
      }
    }
  }
}
```

#### Published Servers

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

## Quickstart

### 1. Install Dependencies

```bash
# Install py-trello for direct API integration
uv add py-trello
```

### 2. Configure Trello (Optional)

Set up environment variables for Trello integration:
```bash
export TRELLO_API_KEY="your_api_key"
export TRELLO_TOKEN="your_token"
export TRELLO_WORKING_BOARD_ID="your_board_id"
```

### 3. Start Using

The system will automatically:
- Detect available Trello integration modes
- Initialize in the best available mode
- Provide fallback to local storage if needed

## Usage Examples

### Create and Assign a Task

```json
{
  "title": "Implement user authentication",
  "description": "Add OAuth2 authentication to the application",
  "dependencies": [],
  "create_trello_card": true
}
```

### Check System Status

```json
{}
```

### Sync to Trello

```json
{}
```

## Development

### Building and Publishing

#### Quick Publish

```bash
# Test locally
npm pack
npm install -g ./daymanking990-task-orchectrator-mcp-0.2.0.tgz

# Publish to npm
npm publish --access public
```

#### Manual Process

1. Update version in `package.json`, `pyproject.toml`, and `__init__.py`

2. Test locally:
```bash
npm pack
npm install -g ./daymanking990-task-orchectrator-mcp-0.2.0.tgz
task-orchectrator-mcp
```

3. Publish to npm:
```bash
npm publish --access public
```

#### GitHub Actions

The package is automatically published to npm when you create a GitHub release. See [Build and Publish Guide](docs/BUILD_AND_PUBLISH.md) for details.

### Debugging

Use the MCP Inspector for debugging:

```bash
npx @modelcontextprotocol/inspector uv --directory C:\Users\xella\PycharmProjects\task-orchectrator-mcp run task-orchectrator-mcp
```

## Documentation

- [Trello Integration Guide](docs/TRELLO_INTEGRATION_GUIDE.md) - Complete guide to Trello integration modes
- [Role System Guide](docs/ROLE_SYSTEM_GUIDE.md) - Detailed role management documentation
- [MCP Setup Instructions](docs/MCP_SETUP_INSTRUCTIONS.md) - MCP server configuration guide
- [Build and Publish Guide](docs/BUILD_AND_PUBLISH.md) - How to build and publish the package

## Architecture

The system uses a three-tier architecture for Trello integration:

1. **MCP Server Layer**: Highest priority, uses MCP protocol for Trello operations
2. **Direct API Layer**: Fallback to direct Trello API calls
3. **Local Storage Layer**: Final fallback with JSON file persistence

All data is automatically synchronized between layers when possible, ensuring data integrity and availability.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.