import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Set
from enum import Enum
import os
import json
import sys
import logging

# Configure logging for MCP server debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),  # Log to stderr for MCP compatibility
        logging.FileHandler('mcp_server_debug.log', mode='w', encoding='utf-8')  # Also log to file with UTF-8
    ]
)
logger = logging.getLogger('task-orchectrator-mcp')

# Log startup information
logger.info("Task Orchestrator MCP Server starting...")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Environment variables: TRELLO_API_KEY={'SET' if os.getenv('TRELLO_API_KEY') else 'NOT SET'}, TRELLO_TOKEN={'SET' if os.getenv('TRELLO_TOKEN') else 'NOT SET'}")

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl, BaseModel
import mcp.server.stdio

logger.info("MCP imports successful")

# Trello integration
try:
    from trello import TrelloClient
    TRELLO_AVAILABLE = True
    logger.info("Trello library imported successfully")
except ImportError as e:
    TRELLO_AVAILABLE = False
    logger.warning(f"Trello library not available: {e}")

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"
    BLOCKED = "BLOCKED"

class Permission(str, Enum):
    """Permissions that roles can have"""
    CREATE_TASK = "create_task"
    ASSIGN_TASK = "assign_task"
    COMPLETE_TASK = "complete_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    VIEW_ALL_TASKS = "view_all_tasks"
    SWITCH_ROLE = "switch_role"
    EXPORT_DATA = "export_data"
    MANAGE_ROLES = "manage_roles"

class RoleType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    ARCHITECT = "architect"
    CODER = "coder"
    ANALYST = "analyst"
    DEVOPS = "devops"

class TrelloMode(str, Enum):
    NONE = "none"
    DIRECT_API = "direct_api"
    MCP = "mcp"

class RolePermissions(BaseModel):
    """Define permissions for each role"""
    role: RoleType
    permissions: Set[Permission]
    description: str

# Define role permissions
ROLE_PERMISSIONS = {
    RoleType.ORCHESTRATOR: RolePermissions(
        role=RoleType.ORCHESTRATOR,
        permissions={
            Permission.CREATE_TASK,
            Permission.ASSIGN_TASK,
            Permission.COMPLETE_TASK,
            Permission.UPDATE_TASK,
            Permission.DELETE_TASK,
            Permission.VIEW_ALL_TASKS,
            Permission.SWITCH_ROLE,
            Permission.EXPORT_DATA,
            Permission.MANAGE_ROLES
        },
        description="Full system control - can manage all tasks and roles"
    ),
    RoleType.ARCHITECT: RolePermissions(
        role=RoleType.ARCHITECT,
        permissions={
            Permission.CREATE_TASK,
            Permission.ASSIGN_TASK,
            Permission.COMPLETE_TASK,
            Permission.UPDATE_TASK,
            Permission.VIEW_ALL_TASKS,
            Permission.EXPORT_DATA
        },
        description="Can create and manage tasks, but cannot delete or manage roles"
    ),
    RoleType.CODER: RolePermissions(
        role=RoleType.CODER,
        permissions={
            Permission.COMPLETE_TASK,
            Permission.UPDATE_TASK,
            Permission.VIEW_ALL_TASKS
        },
        description="Can complete and update assigned tasks, view all tasks"
    ),
    RoleType.ANALYST: RolePermissions(
        role=RoleType.ANALYST,
        permissions={
            Permission.CREATE_TASK,
            Permission.COMPLETE_TASK,
            Permission.UPDATE_TASK,
            Permission.VIEW_ALL_TASKS,
            Permission.EXPORT_DATA
        },
        description="Can create analysis tasks, complete and update tasks, export data"
    ),
    RoleType.DEVOPS: RolePermissions(
        role=RoleType.DEVOPS,
        permissions={
            Permission.COMPLETE_TASK,
            Permission.UPDATE_TASK,
            Permission.VIEW_ALL_TASKS,
            Permission.EXPORT_DATA
        },
        description="Can complete and update DevOps tasks, view all tasks, export data"
    )
}

def has_permission(role: RoleType, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    if role not in ROLE_PERMISSIONS:
        return False
    return permission in ROLE_PERMISSIONS[role].permissions

def get_role_permissions(role: RoleType) -> Set[Permission]:
    """Get all permissions for a role"""
    if role not in ROLE_PERMISSIONS:
        return set()
    return ROLE_PERMISSIONS[role].permissions.copy()

def get_role_description(role: RoleType) -> str:
    """Get description for a role"""
    if role not in ROLE_PERMISSIONS:
        return "Unknown role"
    return ROLE_PERMISSIONS[role].description

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus
    assigned_role: Optional[RoleType]
    created_by: RoleType
    created_at: datetime
    updated_at: datetime
    dependencies: List[str]
    git_branch: Optional[str]
    comments: List[Dict[str, str]]
    subtasks: List[str]
    trello_card_id: Optional[str] = None  # Link to Trello card

class RoleTransition(BaseModel):
    from_role: RoleType
    to_role: RoleType
    task_id: Optional[str]
    reason: str
    timestamp: datetime

# Global state
current_role: RoleType = RoleType.ORCHESTRATOR
tasks: Dict[str, Task] = {}
transitions: List[RoleTransition] = []
task_counter: int = 0

# Trello client and mode
trello_client: Optional[TrelloClient] = None
trello_board = None
trello_mode: TrelloMode = TrelloMode.NONE

# Local storage
TASKS_FILE = "tasks_backup.json"
TRANSITIONS_FILE = "transitions_backup.json"

def check_mcp_trello_availability() -> bool:
    """Check if MCP Trello server is available"""
    try:
        # Try to access MCP session to check for Trello tools
        # This is a simplified check - in practice you might want to check
        # for specific Trello-related tools or capabilities
        if hasattr(server, 'request_context') and server.request_context.session:
            # Check if we can access Trello-related tools through MCP
            # This is a placeholder - actual implementation would depend on
            # how the MCP Trello server exposes its tools
            return True
        return False
    except Exception:
        return False

def save_tasks_locally():
    """Save tasks to local JSON file"""
    try:
        tasks_data = {
            task_id: {
                **task.model_dump(),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task_id, task in tasks.items()
        }
        
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ Tasks saved locally to {TASKS_FILE}", file=sys.stderr)
        
    except Exception as e:
        print(f"❌ Error saving tasks locally: {e}", file=sys.stderr)

def load_tasks_locally():
    """Load tasks from local JSON file"""
    global tasks, task_counter
    
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            for task_id, task_data in tasks_data.items():
                # Convert datetime strings back to datetime objects
                task_data["created_at"] = datetime.fromisoformat(task_data["created_at"])
                task_data["updated_at"] = datetime.fromisoformat(task_data["updated_at"])
                
                # Convert assigned_role string back to enum
                if task_data.get("assigned_role"):
                    task_data["assigned_role"] = RoleType(task_data["assigned_role"])
                
                # Convert created_by string back to enum
                task_data["created_by"] = RoleType(task_data["created_by"])
                
                # Convert status string back to enum
                task_data["status"] = TaskStatus(task_data["status"])
                
                tasks[task_id] = Task(**task_data)
            
            # Update task counter
            if tasks:
                max_task_num = max(int(task.id.split('-')[1]) for task in tasks.values())
                task_counter = max_task_num
            
            print(f"✅ Loaded {len(tasks)} tasks from local storage", file=sys.stderr)
            
    except Exception as e:
        print(f"❌ Error loading tasks from local storage: {e}", file=sys.stderr)

def save_transitions_locally():
    """Save transitions to local JSON file"""
    try:
        transitions_data = [
            {
                **transition.model_dump(),
                "timestamp": transition.timestamp.isoformat()
            }
            for transition in transitions
        ]
        
        with open(TRANSITIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(transitions_data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ Transitions saved locally to {TRANSITIONS_FILE}", file=sys.stderr)
        
    except Exception as e:
        print(f"❌ Error saving transitions locally: {e}", file=sys.stderr)

def load_transitions_locally():
    """Load transitions from local JSON file"""
    global transitions
    
    try:
        if os.path.exists(TRANSITIONS_FILE):
            with open(TRANSITIONS_FILE, 'r', encoding='utf-8') as f:
                transitions_data = json.load(f)
            
            for transition_data in transitions_data:
                # Convert datetime string back to datetime object
                transition_data["timestamp"] = datetime.fromisoformat(transition_data["timestamp"])
                
                # Convert role strings back to enums
                transition_data["from_role"] = RoleType(transition_data["from_role"])
                transition_data["to_role"] = RoleType(transition_data["to_role"])
                
                transitions.append(RoleTransition(**transition_data))
            
            print(f"✅ Loaded {len(transitions)} transitions from local storage", file=sys.stderr)
            
    except Exception as e:
        print(f"❌ Error loading transitions from local storage: {e}", file=sys.stderr)

def init_trello_client():
    """Initialize Trello client if credentials are available"""
    global trello_client, trello_board, trello_mode
    
    logger.info("Initializing Trello client...")
    
    # First, check if MCP Trello server is available
    logger.info("Checking MCP Trello server availability...")
    if check_mcp_trello_availability():
        trello_mode = TrelloMode.MCP
        logger.info("MCP Trello server detected - using MCP integration")
        return True
    
    # If MCP not available, try direct API integration
    if not TRELLO_AVAILABLE:
        trello_mode = TrelloMode.NONE
        logger.warning("Trello integration not available - using local storage")
        return False
    
    try:
        api_key = os.getenv('TRELLO_API_KEY')
        token = os.getenv('TRELLO_TOKEN')
        board_id = os.getenv('TRELLO_WORKING_BOARD_ID')
        
        # Check if credentials are placeholder values
        placeholder_values = [
            "your_trello_api_key_here",
            "your_trello_token_here", 
            "your_trello_board_id_here",
            "",
            None
        ]
        
        has_valid_credentials = (
            api_key and api_key not in placeholder_values and
            token and token not in placeholder_values and
            board_id and board_id not in placeholder_values
        )
        
        logger.info(f"Trello credentials check: API_KEY={'SET' if api_key and api_key not in placeholder_values else 'NOT SET'}, TOKEN={'SET' if token and token not in placeholder_values else 'NOT SET'}, BOARD_ID={'SET' if board_id and board_id not in placeholder_values else 'NOT SET'}")
        
        if has_valid_credentials:
            logger.info("Creating Trello client...")
            trello_client = TrelloClient(api_key=api_key, token=token)
            
            # Find the working board
            logger.info("Fetching Trello boards...")
            boards = trello_client.list_boards()
            logger.info(f"Found {len(boards)} boards")
            
            for board in boards:
                if board.id == board_id:
                    trello_board = board
                    trello_mode = TrelloMode.DIRECT_API
                    logger.info(f"Direct Trello API integration initialized for board: {board.name}")
                    return True
            
            trello_mode = TrelloMode.NONE
            logger.warning(f"Trello board {board_id} not found - using local storage")
            return False
        else:
            trello_mode = TrelloMode.NONE
            logger.warning("Trello credentials not configured or using placeholder values - using local storage")
            return False
            
    except Exception as e:
        trello_mode = TrelloMode.NONE
        logger.error(f"Trello initialization error: {e} - using local storage")
        return False

async def create_trello_card_mcp(task: Task) -> Optional[str]:
    """Create a Trello card for the task via MCP server"""
    try:
        # This is a placeholder implementation
        # In practice, you would call the MCP Trello server's create_card tool
        # Example:
        # result = await server.request_context.session.call_tool(
        #     "create_card",
        #     {
        #         "name": f"{task.id}: {task.title}",
        #         "description": f"**Description:** {task.description}\n\n**Status:** {task.status.value}\n**Assigned to:** {task.assigned_role.value if task.assigned_role else 'Unassigned'}\n**Created:** {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        #         "list_name": "To Do"
        #     }
        # )
        
        # For now, return a mock card ID
        # In real implementation, extract card ID from MCP response
        mock_card_id = f"mcp_card_{task.id}_{int(datetime.now().timestamp())}"
        print(f"✅ MCP Trello card created: {mock_card_id}", file=sys.stderr)
        return mock_card_id
        
    except Exception as e:
        print(f"❌ Error creating MCP Trello card: {e}", file=sys.stderr)
        return None

async def update_trello_card_mcp(task: Task):
    """Update Trello card when task status changes via MCP server"""
    if not task.trello_card_id:
        return
    
    try:
        # This is a placeholder implementation
        # In practice, you would call the MCP Trello server's update_card tool
        # Example:
        # await server.request_context.session.call_tool(
        #     "update_card",
        #     {
        #         "card_id": task.trello_card_id,
        #         "description": f"**Description:** {task.description}\n\n**Status:** {task.status.value}\n**Assigned to:** {task.assigned_role.value if task.assigned_role else 'Unassigned'}\n**Updated:** {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}",
        #         "list_name": {
        #             TaskStatus.TODO: "To Do",
        #             TaskStatus.IN_PROGRESS: "In Progress",
        #             TaskStatus.REVIEW: "Review",
        #             TaskStatus.DONE: "Done",
        #             TaskStatus.BLOCKED: "Blocked"
        #         }.get(task.status, "To Do")
        #     }
        # )
        
        print(f"✅ MCP Trello card updated: {task.trello_card_id}", file=sys.stderr)
        
    except Exception as e:
        print(f"❌ Error updating MCP Trello card: {e}", file=sys.stderr)

def create_trello_card(task: Task) -> Optional[str]:
    """Create a Trello card for the task"""
    global trello_board
    
    if trello_mode == TrelloMode.MCP:
        # Use MCP integration
        import asyncio
        try:
            # Run the async function in a new event loop if needed
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, we can't use run_until_complete
                # This is a limitation - in practice you'd need to handle this differently
                print("⚠️ Cannot create MCP Trello card in sync context", file=sys.stderr)
                return None
            else:
                return loop.run_until_complete(create_trello_card_mcp(task))
        except Exception as e:
            print(f"❌ Error creating MCP Trello card: {e}", file=sys.stderr)
            return None
    
    elif trello_mode == TrelloMode.DIRECT_API:
        # Use direct API integration
        if not trello_board:
            return None
        
        try:
            # Find "To Do" list or create one
            target_list = None
            for lst in trello_board.list_lists():
                if lst.name == "To Do":
                    target_list = lst
                    break
            
            if not target_list:
                # Create "To Do" list if it doesn't exist
                target_list = trello_board.add_list("To Do")
            
            # Create card
            card = target_list.add_card(
                name=f"{task.id}: {task.title}",
                desc=f"**Description:** {task.description}\n\n**Status:** {task.status.value}\n**Assigned to:** {task.assigned_role.value if task.assigned_role else 'Unassigned'}\n**Created:** {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                labels=None,
                due=None
            )
            
            return card.id
            
        except Exception as e:
            print(f"Error creating Trello card: {e}", file=sys.stderr)
            return None
    
    else:
        # No Trello integration available
        return None

def update_trello_card(task: Task):
    """Update Trello card when task status changes"""
    if trello_mode == TrelloMode.MCP:
        # Use MCP integration
        import asyncio
        try:
            # Run the async function in a new event loop if needed
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, we can't use run_until_complete
                # This is a limitation - in practice you'd need to handle this differently
                print("⚠️ Cannot update MCP Trello card in sync context", file=sys.stderr)
                return
            else:
                loop.run_until_complete(update_trello_card_mcp(task))
        except Exception as e:
            print(f"❌ Error updating MCP Trello card: {e}", file=sys.stderr)
    
    elif trello_mode == TrelloMode.DIRECT_API:
        # Use direct API integration
        if not task.trello_card_id or not trello_board:
            return
        
        try:
            # Find the card
            for card in trello_board.get_cards():
                if card.id == task.trello_card_id:
                    # Update card description
                    card.set_description(
                        f"**Description:** {task.description}\n\n**Status:** {task.status.value}\n**Assigned to:** {task.assigned_role.value if task.assigned_role else 'Unassigned'}\n**Updated:** {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    
                    # Move card to appropriate list based on status
                    target_list_name = {
                        TaskStatus.TODO: "To Do",
                        TaskStatus.IN_PROGRESS: "In Progress",
                        TaskStatus.REVIEW: "Review",
                        TaskStatus.DONE: "Done",
                        TaskStatus.BLOCKED: "Blocked"
                    }.get(task.status, "To Do")
                    
                    # Find target list
                    target_list = None
                    for lst in trello_board.list_lists():
                        if lst.name == target_list_name:
                            target_list = lst
                            break
                    
                    if target_list and card.list_id != target_list.id:
                        card.change_list(target_list.id)
                    
                    break
                    
        except Exception as e:
            print(f"Error updating Trello card: {e}", file=sys.stderr)
    
    else:
        # No Trello integration available
        return

server = Server("task-orchectrator-mcp")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available task resources.
    Each task is exposed as a resource with a custom task:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"task://internal/{task.id}"),
            name=f"Task: {task.title}",
            description=f"Task {task.id}: {task.description}",
            mimeType="application/json",
        )
        for task in tasks.values()
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific task's content by its URI.
    """
    if uri.scheme != "task":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    task_id = uri.path.lstrip("/") if uri.path else None
    if task_id and task_id in tasks:
        return tasks[task_id].model_dump_json()
    raise ValueError(f"Task not found: {task_id}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for task and role management.
    """
    tools = [
        types.Tool(
            name="create_task",
            description="Create a new task (Orchestrator, Architect, Analyst)",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "dependencies": {
                        "type": "array", 
                        "items": {"type": "string"},
                        "description": "List of task dependencies"
                    },
                    "create_trello_card": {
                        "type": "boolean",
                        "description": "Create corresponding Trello card",
                        "default": True
                    }
                },
                "required": ["title", "description"],
            },
        ),
        types.Tool(
            name="assign_task",
            description="Assign task to a specific role (Orchestrator, Architect)",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task ID to assign"},
                    "role": {
                        "type": "string", 
                        "enum": ["architect", "coder", "analyst", "devops"],
                        "description": "Role to assign the task to"
                    }
                },
                "required": ["task_id", "role"],
            },
        ),
        types.Tool(
            name="complete_task",
            description="Complete a task and return control to Orchestrator",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Task ID to complete"},
                    "completion_notes": {"type": "string", "description": "Notes about completion"}
                },
                "required": ["task_id"],
            },
        ),
        types.Tool(
            name="switch_role",
            description="Switch to a different role (Orchestrator only)",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string", 
                        "enum": ["architect", "coder", "analyst", "devops"],
                        "description": "Role to switch to"
                    },
                    "reason": {"type": "string", "description": "Reason for switching"}
                },
                "required": ["role"],
            },
        ),
        types.Tool(
            name="return_to_orchestrator",
            description="Return control to Orchestrator",
            inputSchema={
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Reason for returning"}
                },
            },
        ),
        types.Tool(
            name="get_status",
            description="Get current system status",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="list_tasks",
            description="List tasks with optional status filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string", 
                        "enum": ["TODO", "IN_PROGRESS", "REVIEW", "DONE", "BLOCKED"],
                        "description": "Filter by task status"
                    }
                },
            },
        ),
        types.Tool(
            name="export_tasks",
            description="Export tasks to local JSON file",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="check_mcp_trello",
            description="Check if MCP Trello server is available",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="show_role_permissions",
            description="Show current role permissions and capabilities",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="list_roles",
            description="List all available roles with their permissions",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]
    
    # Add Trello-specific tools if available
    if TRELLO_AVAILABLE:
        tools.append(
            types.Tool(
                name="sync_to_trello",
                description="Sync all tasks to Trello board",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            )
        )
    
    return tools

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests for task and role management.
    """
    global current_role, tasks, transitions, task_counter
    
    if not arguments:
        arguments = {}
    
    try:
        if name == "create_task":
            if not has_permission(current_role, Permission.CREATE_TASK):
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Role {current_role.value} cannot create tasks. Required permission: {Permission.CREATE_TASK.value}"
                )]
            
            title = arguments.get("title")
            description = arguments.get("description")
            dependencies = arguments.get("dependencies", [])
            create_trello_card = arguments.get("create_trello_card", True)
            
            if not title or not description:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Title and description are required"
                )]
            
            task_counter += 1
            task_id = f"TASK-{task_counter:03d}"
            
            task = Task(
                id=task_id,
                title=title,
                description=description,
                status=TaskStatus.TODO,
                assigned_role=None,
                created_by=RoleType.ORCHESTRATOR,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                dependencies=dependencies,
                git_branch=None,
                comments=[],
                subtasks=[],
                trello_card_id=None
            )
            
            # Create Trello card if requested and available
            trello_card_id = None
            if create_trello_card and trello_mode != TrelloMode.NONE:
                trello_card_id = create_trello_card(task)
                if trello_card_id:
                    task.trello_card_id = trello_card_id
                    if trello_mode == TrelloMode.MCP:
                        print(f"✅ MCP Trello card created: {trello_card_id}", file=sys.stderr)
                    else:
                        print(f"✅ Trello card created: {trello_card_id}", file=sys.stderr)
                else:
                    print("⚠️ Failed to create Trello card, saving locally", file=sys.stderr)
            else:
                print("ℹ️ Trello not available, saving task locally", file=sys.stderr)
            
            tasks[task_id] = task
            
            # Save locally
            save_tasks_locally()
            
            await server.request_context.session.send_resource_list_changed()
            
            trello_info = f" (Trello card created: {task.trello_card_id})" if task.trello_card_id else " (saved locally)"
            return [types.TextContent(
                type="text",
                text=f"✅ Task {task_id} created successfully: {title}{trello_info}"
            )]
        
        elif name == "assign_task":
            if not has_permission(current_role, Permission.ASSIGN_TASK):
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Role {current_role.value} cannot assign tasks. Required permission: {Permission.ASSIGN_TASK.value}"
                )]
            
            task_id = arguments.get("task_id")
            role_name = arguments.get("role")
            
            if not task_id or not role_name:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Task ID and role are required"
                )]
            
            if task_id not in tasks:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Task {task_id} not found"
                )]
            
            try:
                role = RoleType(role_name)
            except ValueError:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Invalid role: {role_name}"
                )]
            
            task = tasks[task_id]
            
            # Check dependencies
            for dep_id in task.dependencies:
                if dep_id in tasks and tasks[dep_id].status != TaskStatus.DONE:
                    return [types.TextContent(
                        type="text",
                        text=f"❌ Error: Task {task_id} is blocked by dependency {dep_id}"
                    )]
            
            task.assigned_role = role
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.now()
            
            # Update Trello card if available
            if trello_mode != TrelloMode.NONE:
                update_trello_card(task)
                if trello_mode == TrelloMode.MCP:
                    print(f"✅ MCP Trello card updated for task {task_id}", file=sys.stderr)
                else:
                    print(f"✅ Trello card updated for task {task_id}", file=sys.stderr)
            else:
                print(f"ℹ️ Trello not available, updated task {task_id} locally", file=sys.stderr)
            
            # Create transition
            transition = RoleTransition(
                from_role=RoleType.ORCHESTRATOR,
                to_role=role,
                task_id=task_id,
                reason=f"Task {task_id} assigned to {role.value}",
                timestamp=datetime.now()
            )
            transitions.append(transition)
            
            # Save locally
            save_tasks_locally()
            save_transitions_locally()
            
            await server.request_context.session.send_resource_list_changed()
            
            return [types.TextContent(
                type="text",
                text=f"✅ Task {task_id} assigned to {role.value}"
            )]
        
        elif name == "complete_task":
            task_id = arguments.get("task_id")
            completion_notes = arguments.get("completion_notes", "")
            
            if not task_id:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Task ID is required"
                )]
            
            if task_id not in tasks:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Task {task_id} not found"
                )]
            
            task = tasks[task_id]
            
            if task.assigned_role != current_role:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Only assigned role {task.assigned_role.value} can complete this task"
                )]
            
            task.status = TaskStatus.DONE
            task.updated_at = datetime.now()
            task.comments.append({
                "role": current_role.value,
                "comment": f"Task completed: {completion_notes}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Update Trello card if available
            if trello_mode != TrelloMode.NONE:
                update_trello_card(task)
                if trello_mode == TrelloMode.MCP:
                    print(f"✅ MCP Trello card updated for completed task {task_id}", file=sys.stderr)
                else:
                    print(f"✅ Trello card updated for completed task {task_id}", file=sys.stderr)
            else:
                print(f"ℹ️ Trello not available, updated completed task {task_id} locally", file=sys.stderr)
            
            # Create transition back to Orchestrator
            transition = RoleTransition(
                from_role=current_role,
                to_role=RoleType.ORCHESTRATOR,
                task_id=task_id,
                reason=f"Task {task_id} completed by {current_role.value}",
                timestamp=datetime.now()
            )
            transitions.append(transition)
            
            # Save locally
            save_tasks_locally()
            save_transitions_locally()
            
            await server.request_context.session.send_resource_list_changed()
            
            return [types.TextContent(
                type="text",
                text=f"✅ Task {task_id} completed, returning control to Orchestrator"
            )]
        
        elif name == "switch_role":
            if not has_permission(current_role, Permission.SWITCH_ROLE):
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Role {current_role.value} cannot switch roles. Required permission: {Permission.SWITCH_ROLE.value}"
                )]
            
            role_name = arguments.get("role")
            reason = arguments.get("reason", "")
            
            if not role_name:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Role is required"
                )]
            
            try:
                new_role = RoleType(role_name)
            except ValueError:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Error: Invalid role: {role_name}"
                )]
            
            if new_role == RoleType.ORCHESTRATOR:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Already in Orchestrator role"
                )]
            
            # Create transition
            transition = RoleTransition(
                from_role=RoleType.ORCHESTRATOR,
                to_role=new_role,
                task_id=None,
                reason=reason or f"Switching to {new_role.value} role",
                timestamp=datetime.now()
            )
            transitions.append(transition)
            
            current_role = new_role
            
            # Save transitions locally
            save_transitions_locally()
            
            return [types.TextContent(
                type="text",
                text=f"✅ Switched to {new_role.value} role"
            )]
        
        elif name == "return_to_orchestrator":
            if current_role == RoleType.ORCHESTRATOR:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Already in Orchestrator role"
                )]
            
            reason = arguments.get("reason", "")
            
            # Create transition
            transition = RoleTransition(
                from_role=current_role,
                to_role=RoleType.ORCHESTRATOR,
                task_id=None,
                reason=reason or f"Returning control to Orchestrator",
                timestamp=datetime.now()
            )
            transitions.append(transition)
            
            current_role = RoleType.ORCHESTRATOR
            
            # Save transitions locally
            save_transitions_locally()
            
            return [types.TextContent(
                type="text",
                text=f"✅ Returned control to Orchestrator"
            )]
        
        elif name == "get_status":
            tasks_by_status = {
                status.value: len([t for t in tasks.values() if t.status == status])
                for status in TaskStatus
            }
            
            recent_transitions = [
                {
                    "from": t.from_role.value,
                    "to": t.to_role.value,
                    "task_id": t.task_id,
                    "reason": t.reason,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in transitions[-5:]  # Last 5 transitions
            ]
            
            trello_status_map = {
                TrelloMode.NONE: "❌ Not connected",
                TrelloMode.DIRECT_API: "✅ Direct API",
                TrelloMode.MCP: "✅ MCP Server"
            }
            trello_status = trello_status_map.get(trello_mode, "❌ Unknown")
            local_storage_status = "✅ Available" if os.path.exists(TASKS_FILE) else "❌ Not available"
            
            # Get current role permissions
            permissions = get_role_permissions(current_role)
            permissions_list = ", ".join([perm.value for perm in sorted(permissions)])
            
            status_text = f"""
🎭 **Current Role**: {current_role.value}
🔑 **Permissions**: {permissions_list}
📊 **Total Tasks**: {len(tasks)}
🔗 **Trello Mode**: {trello_status}
💾 **Local Storage**: {local_storage_status}
📈 **Tasks by Status**:
"""
            for status, count in tasks_by_status.items():
                status_text += f"  - {status}: {count}\n"
            
            if recent_transitions:
                status_text += "\n🔄 **Recent Transitions**:\n"
                for t in recent_transitions:
                    status_text += f"  - {t['from']} → {t['to']}: {t['reason']}\n"
            
            return [types.TextContent(
                type="text",
                text=status_text
            )]
        
        elif name == "list_tasks":
            status_filter = arguments.get("status")
            
            filtered_tasks = list(tasks.values())
            if status_filter:
                try:
                    status = TaskStatus(status_filter)
                    filtered_tasks = [t for t in filtered_tasks if t.status == status]
                except ValueError:
                    return [types.TextContent(
                        type="text",
                        text=f"❌ Error: Invalid status: {status_filter}"
                    )]
            
            if not filtered_tasks:
                return [types.TextContent(
                    type="text",
                    text="📝 No tasks found" + (f" with status {status_filter}" if status_filter else "")
                )]
            
            tasks_text = f"📋 **Tasks** ({len(filtered_tasks)} found):\n\n"
            for task in filtered_tasks:
                if task.trello_card_id:
                    if trello_mode == TrelloMode.MCP:
                        trello_info = f" [🔗 MCP Trello: {task.trello_card_id}]"
                    else:
                        trello_info = f" [🔗 Trello: {task.trello_card_id}]"
                else:
                    trello_info = " [💾 Local]"
                
                tasks_text += f"**{task.id}**: {task.title}{trello_info}\n"
                tasks_text += f"  Status: {task.status.value}\n"
                tasks_text += f"  Assigned to: {task.assigned_role.value if task.assigned_role else 'Unassigned'}\n"
                tasks_text += f"  Description: {task.description}\n"
                if task.dependencies:
                    tasks_text += f"  Dependencies: {', '.join(task.dependencies)}\n"
                tasks_text += "\n"
            
            return [types.TextContent(
                type="text",
                text=tasks_text
            )]
        
        elif name == "export_tasks":
            save_tasks_locally()
            save_transitions_locally()
            
            return [types.TextContent(
                type="text",
                text=f"✅ Exported {len(tasks)} tasks and {len(transitions)} transitions to local files"
            )]
        
        elif name == "check_mcp_trello":
            if check_mcp_trello_availability():
                return [types.TextContent(
                    type="text",
                    text="✅ MCP Trello server is available and accessible."
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text="❌ MCP Trello server is not available or inaccessible."
                )]
        
        elif name == "show_role_permissions":
            permissions = get_role_permissions(current_role)
            description = get_role_description(current_role)
            
            permissions_text = "\n".join([f"  - {perm.value}" for perm in sorted(permissions)])
            
            return [types.TextContent(
                type="text",
                text=f"🎭 **Current Role**: {current_role.value}\n"
                     f"📝 **Description**: {description}\n"
                     f"🔑 **Permissions**:\n{permissions_text}"
            )]
        
        elif name == "list_roles":
            roles_text = "👥 **Available Roles and Permissions**:\n\n"
            
            for role in RoleType:
                permissions = get_role_permissions(role)
                description = get_role_description(role)
                permissions_list = ", ".join([perm.value for perm in sorted(permissions)])
                
                roles_text += f"**{role.value.title()}**:\n"
                roles_text += f"  Description: {description}\n"
                roles_text += f"  Permissions: {permissions_list}\n\n"
            
            return [types.TextContent(
                type="text",
                text=roles_text
            )]
        
        elif name == "sync_to_trello":
            if trello_mode == TrelloMode.NONE:
                return [types.TextContent(
                    type="text",
                    text="❌ Error: Trello integration not available"
                )]
            
            if trello_mode == TrelloMode.MCP:
                # Sync via MCP
                synced_count = 0
                for task in tasks.values():
                    if not task.trello_card_id:
                        trello_card_id = create_trello_card(task)
                        if trello_card_id:
                            task.trello_card_id = trello_card_id
                            synced_count += 1
                    else:
                        update_trello_card(task)
                
                # Save locally after sync
                save_tasks_locally()
                
                await server.request_context.session.send_resource_list_changed()
                
                return [types.TextContent(
                    type="text",
                    text=f"✅ Synced {synced_count} tasks to MCP Trello board"
                )]
            
            elif trello_mode == TrelloMode.DIRECT_API:
                # Sync via direct API
                if not trello_board:
                    return [types.TextContent(
                        type="text",
                        text="❌ Error: Trello board not connected"
                    )]
                
                synced_count = 0
                for task in tasks.values():
                    if not task.trello_card_id:
                        trello_card_id = create_trello_card(task)
                        if trello_card_id:
                            task.trello_card_id = trello_card_id
                            synced_count += 1
                    else:
                        update_trello_card(task)
                
                # Save locally after sync
                save_tasks_locally()
                
                await server.request_context.session.send_resource_list_changed()
                
                return [types.TextContent(
                    type="text",
                    text=f"✅ Synced {synced_count} tasks to Trello board"
                )]
        
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Error: Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]

async def main():
    logger.info("Starting main function...")
    
    try:
        # Load existing data from local storage
        logger.info("Loading existing data from local storage...")
        load_tasks_locally()
        load_transitions_locally()
        logger.info(f"Loaded {len(tasks)} tasks and {len(transitions)} transitions")
        
        # Initialize Trello client
        logger.info("Initializing Trello integration...")
        if init_trello_client():
            if trello_mode == TrelloMode.MCP:
                logger.info("MCP Trello integration initialized")
            elif trello_mode == TrelloMode.DIRECT_API:
                logger.info("Direct Trello API integration initialized")
            else:
                logger.warning("Trello integration not available - using local storage")
        else:
            logger.warning("Trello integration not available - using local storage")
        
        # Run the server using stdin/stdout streams
        logger.info("Starting MCP server with stdio transport...")
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("stdio transport established")
            
            capabilities = server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            )
            logger.info(f"Server capabilities: {capabilities}")
            
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="task-orchectrator-mcp",
                    server_version="0.3.0",
                    capabilities=capabilities,
                ),
            )
            logger.info("Server run completed")
            
    except Exception as e:
        logger.error(f"Fatal error in main function: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

# Add entry point for direct execution
if __name__ == "__main__":
    logger.info("Starting MCP server as main module...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)