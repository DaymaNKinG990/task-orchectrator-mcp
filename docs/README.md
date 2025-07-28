# Task Orchestrator MCP Server Documentation

Welcome to the Task Orchestrator MCP Server documentation! This guide will help you get started and find the information you need.

## 📚 Documentation Overview

### 🚀 Getting Started
- **[MCP Setup Instructions](MCP_SETUP_INSTRUCTIONS.md)** - Complete setup guide for using the server in Cursor AI and other MCP clients
- **[Quick Publish](QUICK_PUBLISH.md)** - Fast publishing guide for developers

### 🔧 Development & Publishing
- **[Build and Publish](BUILD_AND_PUBLISH.md)** - Comprehensive guide for building and publishing the npm package
- **[MCP Registry Publish](MCP_REGISTRY_PUBLISH.md)** - How to add your server to the official MCP registry

### 🎭 Role System
- **[Role System Guide](ROLE_SYSTEM_GUIDE.md)** - Complete guide to the role-based workflow system
- **[Role Permissions Summary](ROLE_PERMISSIONS_SUMMARY.md)** - Detailed breakdown of role permissions and capabilities

### 🔗 Trello Integration
- **[Trello Integration Guide](TRELLO_INTEGRATION_GUIDE.md)** - Complete guide to Trello integration features
- **[Trello Token Setup](TRELLO_TOKEN_SETUP.md)** - Step-by-step guide for setting up Trello API credentials

## 🎯 Quick Start

### 1. Install the Server
```bash
npm install @daymanking990/task-orchectrator-mcp
```

### 2. Configure MCP Client
Add to your MCP configuration file (e.g., `~/.cursor/mcp.json`):
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

### 3. Start Using
- Create tasks: `"Create task: Implement authentication - Add OAuth2 login"`
- Switch roles: `"Switch to architect mode"`
- View status: `"Show system status"`

## 🔑 Key Features

### Role-Based Workflow
- **Orchestrator**: Full system control and coordination
- **Architect**: System design and architecture
- **Coder**: Implementation and development
- **Analyst**: Research and analysis
- **DevOps**: Infrastructure and deployment

### Trello Integration
- **MCP Server Mode**: Integration via MCP Trello server
- **Direct API Mode**: Direct Trello API integration
- **Local Storage Mode**: Offline task management

### Task Management
- Create, assign, and complete tasks
- Track dependencies and status
- Automatic Trello card creation
- Role-based permissions

## 📖 Documentation Structure

```
docs/
├── README.md                           # This file - documentation index
├── MCP_SETUP_INSTRUCTIONS.md          # Setup guide for MCP clients
├── BUILD_AND_PUBLISH.md               # Development and publishing guide
├── QUICK_PUBLISH.md                   # Quick publishing reference
├── MCP_REGISTRY_PUBLISH.md            # Official registry publishing
├── ROLE_SYSTEM_GUIDE.md               # Role system overview
├── ROLE_PERMISSIONS_SUMMARY.md        # Role permissions details
├── TRELLO_INTEGRATION_GUIDE.md        # Trello integration guide
└── TRELLO_TOKEN_SETUP.md              # Trello API setup
```

## 🆘 Need Help?

### Common Issues
1. **Server won't start**: Check [MCP Setup Instructions](MCP_SETUP_INSTRUCTIONS.md)
2. **Trello integration issues**: See [Trello Token Setup](TRELLO_TOKEN_SETUP.md)
3. **Role permission errors**: Review [Role Permissions Summary](ROLE_PERMISSIONS_SUMMARY.md)
4. **Publishing problems**: Follow [Build and Publish](BUILD_AND_PUBLISH.md)

### Getting Support
- Check the troubleshooting sections in each guide
- Review the error messages for specific guidance
- Ensure all prerequisites are installed (Node.js, uv, npm)

## 🔄 Version Information

- **Current Version**: 0.3.0
- **Latest Features**: Flexible role permission system, improved error handling
- **Compatibility**: MCP protocol v1.0+, Node.js 18+, Python 3.12+

## 📝 Contributing

To contribute to the documentation:
1. Fork the repository
2. Make your changes
3. Submit a pull request
4. Ensure all documentation is in English
5. Remove any sensitive data before committing

---

**Happy orchestrating! 🎼** 