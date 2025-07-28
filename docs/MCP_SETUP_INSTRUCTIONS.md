# 🔧 Task Orchestrator MCP Server Setup

## 📋 What you need to do

### 1. Update MCP Configuration

Replace the contents of your `.../.cursor\mcp.json` file with the following:

```json
{
  "mcpServers": {
    "task-orchestrator": {
      "command": "npx",
      "args": ["@daymanking990/task-orchectrator-mcp"],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key_here",
        "TRELLO_TOKEN": "your_trello_token_here",
        "TRELLO_WORKING_BOARD_ID": "your_trello_board_id_here"
      }
    }
  }
}
```

### 2. Restart Cursor

After updating the configuration, restart Cursor for the changes to take effect.

## 🎮 How to use

### Management commands:

```
"Create task: Add authentication - Implement user login system"
"Switch to analyst mode"
"Switch to architect mode"
"Switch to coder mode"
"Return control to Orchestrator"
"Show system status"
"Show task list"
"Sync tasks with Trello"
```

### Available MCP tools:

- `create_task` - create a task (Orchestrator, Architect, Analyst)
- `assign_task` - assign a task to a role (Orchestrator, Architect)
- `complete_task` - complete a task (current role)
- `switch_role` - switch to another role (Orchestrator only)
- `return_to_orchestrator` - return control to Orchestrator
- `get_status` - get system status
- `list_tasks` - list all tasks
- `sync_to_trello` - sync tasks with Trello (if available)
- `show_role_permissions` - show current role permissions
- `list_roles` - list all available roles

## 🔗 Trello Integration

### Automatic card creation:
- When a task is created, a Trello card is automatically created
- Cards move between lists depending on task status
- Card description is updated when task status changes

### Trello lists:
- **To Do** - new tasks
- **In Progress** - tasks in progress
- **Review** - tasks under review
- **Done** - completed tasks
- **Blocked** - blocked tasks

## 🔍 Verification

After setup, you should see in Cursor:
- New MCP server `task-orchestrator` in the list of available servers
- Ability to use role management commands
- Automatic role switching
- Trello integration (if proper keys are configured)

## 🚨 Possible issues

### 1. File path
Make sure the path in your configuration matches your project structure.

### 2. UV not found
Make sure UV is installed and available in PATH.

### 3. Permissions
Make sure Cursor has permission to execute UV commands.

### 4. Trello API keys
If Trello integration doesn't work:
- Check the correctness of API key and token
- Make sure the board exists and is accessible
- Check board access permissions

## ✅ Done!

After setup, the role-based system will be fully integrated into Cursor and ready to use!

## 🧪 Testing

To test the server, use the command:
```bash
npx @daymanking990/task-orchectrator-mcp
```

The server will start and be ready to work through the MCP protocol.

## 🔧 Additional features

### Trello synchronization:
- Automatic card creation when tasks are created
- Card status updates when task status changes
- Card movement between lists
- Synchronization of all existing tasks

### Dependency management:
- Dependency checking before task assignment
- Blocking tasks with incomplete dependencies
- Tracking relationships between tasks 