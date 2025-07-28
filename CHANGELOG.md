# Changelog

## [0.2.0] - 2024-01-15

### Added
- **Three-tier Trello integration architecture**:
  - **MCP Server Mode** (Priority 1): Integration through MCP Trello server
  - **Direct API Mode** (Priority 2): Direct Trello API integration
  - **Local Storage Mode** (Priority 3): Local JSON storage without Trello
- **Automatic mode detection and fallback** system
- **New tools**:
  - `check_mcp_trello`: Check MCP Trello server availability
- **Enhanced status reporting** with Trello mode information
- **Improved error handling** and graceful degradation
- **npm package support** for easy installation and distribution

### Changed
- **Refactored Trello integration** to support multiple modes
- **Updated initialization logic** to detect best available mode
- **Enhanced logging** with mode-specific messages
- **Improved documentation** with comprehensive integration guide
- **Converted to npm package** for standard MCP server distribution

### Technical Details
- Added `TrelloMode` enum for mode tracking
- Implemented `check_mcp_trello_availability()` function
- Created async MCP wrapper functions (`create_trello_card_mcp`, `update_trello_card_mcp`)
- Modified all Trello operations to support three modes
- Updated status display to show current Trello mode
- Created JavaScript wrapper (`bin/index.js`) for npm package
- Added postinstall script for automatic dependency setup

### Documentation
- Updated `README.md` with comprehensive feature overview
- Enhanced `docs/TRELLO_INTEGRATION_GUIDE.md` with three-mode architecture
- Added usage examples and troubleshooting guides
- Created `docs/BUILD_AND_PUBLISH.md` with npm publication guide
- Added `QUICK_PUBLISH.md` for rapid deployment instructions

## [0.1.0] - 2024-01-14

### Added
- Initial release with role-based task orchestration
- Basic Trello integration (Direct API only)
- Local storage with JSON persistence
- Task lifecycle management
- Role transition tracking 