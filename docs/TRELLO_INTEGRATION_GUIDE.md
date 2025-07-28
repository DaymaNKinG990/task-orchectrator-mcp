# Trello Integration Guide

This guide explains how to set up and use Trello integration with the Task Orchestrator MCP server.

## Overview

The Task Orchestrator supports three different modes for Trello integration:

1. **MCP Server Mode** - Uses an MCP Trello server for integration
2. **Direct API Mode** - Uses direct Trello API integration
3. **Local Storage Mode** - Stores tasks locally without Trello integration

## Mode Selection

The system automatically detects and selects the best available mode:

1. **MCP Server Mode** (Priority 1): If an MCP Trello server is available, it will be used
2. **Direct API Mode** (Priority 2): If MCP server is not available but Trello credentials are configured
3. **Local Storage Mode** (Priority 3): If neither MCP server nor direct API are available

## MCP Server Mode

### Prerequisites
- An MCP Trello server must be available and accessible
- The MCP server should provide tools for creating and updating Trello cards

### Features
- Automatic card creation when tasks are created
- Card updates when task status changes
- Card movement between lists based on task status
- Integration through MCP protocol

### Usage
The system will automatically detect MCP Trello server availability and use it when possible.

## Direct API Mode

### Prerequisites
- Trello API key and token
- Trello board ID
- `py-trello` package installed

### Setup
1. Install the required package:
   ```bash
   uv add py-trello
   ```

2. Set environment variables:
   ```bash
   export TRELLO_API_KEY="your_api_key"
   export TRELLO_TOKEN="your_token"
   export TRELLO_WORKING_BOARD_ID="your_board_id"
   ```

### Features
- Direct integration with Trello API
- Automatic card creation and updates
- Status synchronization
- List management

## Local Storage Mode

### Features
- Tasks stored locally in JSON files
- No external dependencies
- Works offline
- Data persistence across sessions

## Tools

### Available Tools

1. **create_task** - Creates a new task with optional Trello card
2. **assign_task** - Assigns a task to a role and updates Trello
3. **complete_task** - Completes a task and updates Trello
4. **sync_to_trello** - Syncs all tasks to Trello board
5. **check_mcp_trello** - Checks MCP Trello server availability
6. **get_status** - Shows current system status including Trello mode

### Tool Usage Examples

#### Create Task with Trello Card
```json
{
  "title": "Implement user authentication",
  "description": "Add OAuth2 authentication to the application",
  "dependencies": ["TASK-001"],
  "create_trello_card": true
}
```

#### Check MCP Trello Availability
```json
{}
```

#### Sync All Tasks to Trello
```json
{}
```

## Status Information

The `get_status` tool provides information about the current Trello mode:

- **MCP Server**: Shows "✅ MCP Server"
- **Direct API**: Shows "✅ Direct API"  
- **Local Storage**: Shows "❌ Not connected"

## Error Handling

The system gracefully handles failures:

- If MCP server is unavailable, falls back to direct API
- If direct API fails, falls back to local storage
- All operations continue to work regardless of Trello availability
- Error messages are logged to stderr

## Troubleshooting

### MCP Server Not Detected
- Ensure the MCP Trello server is running and accessible
- Check MCP server configuration
- Use `check_mcp_trello` tool to verify availability

### Direct API Issues
- Verify environment variables are set correctly
- Check Trello API credentials
- Ensure the board ID is valid
- Verify network connectivity

### Local Storage Issues
- Check file permissions for JSON files
- Ensure sufficient disk space
- Verify JSON file format integrity

## Best Practices

1. **Always use MCP Server mode when available** - It provides the best integration
2. **Configure fallback options** - Set up direct API as backup
3. **Monitor status regularly** - Use `get_status` to check current mode
4. **Backup local data** - Export tasks regularly with `export_tasks`
5. **Test integration** - Use `check_mcp_trello` to verify setup

## Migration Between Modes

The system automatically handles mode transitions:

1. **MCP → Direct API**: When MCP server becomes unavailable
2. **Direct API → Local**: When API credentials are invalid
3. **Local → MCP/Direct**: When integration becomes available again

All existing data is preserved during mode transitions. 