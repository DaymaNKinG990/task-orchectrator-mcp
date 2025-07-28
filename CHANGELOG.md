# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2025-07-28

### Added
- **Flexible Role Permission System**: Replaced rigid hierarchy with granular permissions
- **Role-based Access Control**: Each role now has specific permissions and capabilities
- **New Tools**: 
  - `show_role_permissions` - Display current role permissions
  - `list_roles` - List all available roles with their permissions
- **Enhanced Role Descriptions**: Each role now has a detailed description of capabilities
- **Permission-based Error Messages**: Clear error messages showing required permissions

### Changed
- **Role Permissions**:
  - **Orchestrator**: Full system control (all permissions)
  - **Architect**: Can create, assign, complete, update tasks, view all tasks, export data
  - **Coder**: Can complete, update tasks, view all tasks
  - **Analyst**: Can create, complete, update tasks, view all tasks, export data
  - **DevOps**: Can complete, update tasks, view all tasks, export data
- **Tool Descriptions**: Updated to show which roles can use each tool
- **Status Display**: Now shows current role permissions in status output

### Technical
- Added `Permission` enum with granular permissions
- Added `RolePermissions` model for role configuration
- Added permission checking functions: `has_permission()`, `get_role_permissions()`, `get_role_description()`
- Updated all tool handlers to use permission-based access control

## [0.2.6] - 2025-07-28

### Fixed
- **Environment Variable Passing**: Fixed issue where Trello credentials were not being passed from Cursor AI to Python server
- **Node.js Wrapper**: Enhanced `bin/index.js` to explicitly pass environment variables to Python subprocess
- **Placeholder Detection**: Added logic to detect placeholder Trello credentials and fall back to local storage

### Changed
- **Trello Integration**: Improved credential handling with placeholder value detection
- **Logging**: Enhanced debugging information for environment variable status

## [0.2.5] - 2025-07-28

### Fixed
- **Character Encoding**: Fixed UnicodeEncodeError by removing emojis from log messages and setting UTF-8 encoding
- **Python Import Conflicts**: Resolved RuntimeWarning by changing execution method in `bin/index.js`

### Changed
- **Logging**: Removed emojis from log messages to prevent encoding issues
- **Server Execution**: Changed from module execution to direct script execution

## [0.2.4] - 2025-07-28

### Added
- **Comprehensive Logging**: Added detailed logging throughout the server lifecycle
- **Debug File**: Created `mcp_server_debug.log` for troubleshooting
- **Startup Information**: Log Python version, working directory, and environment variables

### Changed
- **Error Handling**: Enhanced error handling with specific error types
- **Logging Configuration**: Configured logging to output to both stderr and file

## [0.2.3] - 2025-07-28

### Fixed
- **npm Package**: Fixed package structure and dependencies
- **Python Import Issues**: Resolved module import conflicts
- **File Inclusions**: Fixed `__pycache__` files being included in npm package

### Changed
- **Package Structure**: Improved npm package organization
- **Dependencies**: Removed unnecessary Node.js dependencies

## [0.2.2] - 2025-07-28

### Added
- **npm Package**: Published as npm package `@daymanking990/task-orchectrator-mcp`
- **JavaScript Wrapper**: Created `bin/index.js` for npm package execution
- **Postinstall Script**: Automatic dependency installation via `scripts/postinstall.js`
- **Package Configuration**: Added `package.json` with proper metadata and scripts

### Changed
- **Distribution**: Changed from Python-only to npm-based distribution
- **Installation**: Now installable via `npm install -g @daymanking990/task-orchectrator-mcp`

## [0.2.1] - 2025-07-28

### Added
- **Three-tier Trello Integration**:
  - `NONE`: Local storage only
  - `DIRECT_API`: Direct Trello API integration
  - `MCP`: Integration via external MCP Trello server
- **Trello Mode Detection**: Automatic detection of available Trello integration methods
- **Fallback Logic**: Graceful fallback to local storage when Trello is unavailable
- **MCP Trello Tools**: Added tools for MCP Trello server integration

### Changed
- **Trello Integration**: Completely redesigned to support multiple integration modes
- **Error Handling**: Enhanced error handling for Trello operations
- **Documentation**: Updated Trello integration guide

## [0.2.0] - 2025-07-28

### Added
- **Trello Integration**: Direct API integration with Trello boards
- **Trello Card Management**: Automatic creation and updating of Trello cards
- **Environment Variables**: Support for Trello API credentials via environment variables
- **Board Management**: Automatic board and list creation

### Changed
- **Task Model**: Added `trello_card_id` field for Trello integration
- **Storage**: Enhanced local storage with Trello card IDs
- **Error Handling**: Improved error handling for Trello operations

## [0.1.0] - 2025-07-28

### Added
- **Role-based Task Management**: Orchestrator, Architect, Coder, Analyst, DevOps roles
- **Task Lifecycle**: Create, assign, complete tasks with role transitions
- **Local Storage**: JSON-based local storage for tasks and transitions
- **MCP Server**: Full MCP server implementation with stdio transport
- **Resource Management**: Task resources with custom URI scheme
- **Tool Integration**: Comprehensive set of tools for task management 