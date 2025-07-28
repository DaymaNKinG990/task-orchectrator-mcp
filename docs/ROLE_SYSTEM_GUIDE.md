# 🎭 Role System with Orchestrator

## 📋 System Overview

The role system is built on a hierarchical model where the **Orchestrator** is the main role that manages all other roles.

### 🎯 Main Roles:

1. **🎼 Orchestrator** - main role, coordinator
2. **🏗️ Architect** - architecture design
3. **💻 Coder** - task implementation
4. **🔍 Analyst** - analysis and research
5. **⚙️ DevOps** - infrastructure and configuration

## 🔄 Role Switching Protocol

### Rules:
- **All transitions** between roles go through the Orchestrator
- **Roles cannot** switch directly to each other
- **After completing** work, the role returns control to the Orchestrator
- **The Orchestrator decides** who to pass control to next

## 📝 Task Management

### Task Statuses:
- `TODO` - task created, waiting for assignment
- `IN_PROGRESS` - task in progress
- `REVIEW` - task under review
- `DONE` - task completed
- `BLOCKED` - task blocked by dependencies

### Git Branching Flow:
- **Master** → **Release** → **Feature** branches
- Automatic branch creation for tasks
- Dependency tracking between branches
- Pull Request creation request when needed

## 🎮 Management Commands

### Role Switching:
```bash
# Switch to Architect mode
"Switch to architect mode"

# Switch to Coder mode
"Switch to coder mode"

# Switch to Analyst mode
"Switch to analyst mode"

# Switch to DevOps mode
"Switch to DevOps mode"

# Return to Orchestrator
"Return control to Orchestrator"
```

### Task Management:
```bash
# Create task (Orchestrator only)
"Create task: [title] - [description]"

# Assign task to role (Orchestrator only)
"Assign task TASK-001 to Architect"

# Complete task (current role)
"Complete task TASK-001: [completion notes]"

# Show system status
"Show system status"

# List tasks
"Show task list"
```

## 🔧 Practical Examples

### Example 1: Creating a New Feature
```
Orchestrator → Creates task "Add authentication"
Orchestrator → Assigns to Analyst for research
Analyst → Researches requirements and technologies
Analyst → Returns control to Orchestrator
Orchestrator → Assigns to Architect for design
Architect → Designs authentication architecture
Architect → Returns control to Orchestrator
Orchestrator → Assigns to Coder for implementation
Coder → Implements authentication feature
Coder → Returns control to Orchestrator
Orchestrator → Assigns to DevOps for configuration
DevOps → Configures infrastructure
DevOps → Returns control to Orchestrator
```

### Example 2: Fixing a Bug
```
Orchestrator → Creates task "Fix loading bug"
Orchestrator → Assigns to Analyst for analysis
Analyst → Analyzes bug cause
Analyst → Returns control to Orchestrator
Orchestrator → Assigns to Coder for fixing
Coder → Fixes the bug
Coder → Returns control to Orchestrator
```

## 🎯 Usage Recommendations

### For Orchestrator:
- Always create clear tasks with descriptions
- Check dependencies before assignment
- Track progress of all tasks
- Make decisions about priorities

### For Architect:
- Focus on long-term architecture
- Follow SOLID principles
- Create diagrams and documentation
- Consider scalability

### For Coder:
- Write clean, readable code
- Create tests for new functionality
- Follow best practices
- Optimize performance

### For Analyst:
- Ask clarifying questions
- Research context through Context7
- Analyze requirements
- Suggest improvements

### For DevOps:
- Configure infrastructure
- Create CI/CD pipelines
- Ensure security
- Optimize deployments

## 🚀 Additional Features

### Automation:
- Automatic Git branch creation
- Dependency tracking
- Blocking notifications
- Role transition history

### Monitoring:
- Task statistics
- Role execution time
- Transition efficiency
- Task completion quality

## 🔄 Memory MCP Integration

The system integrates with Memory MCP for:
- Saving context between sessions
- Tracking decision history
- Saving project knowledge
- Managing long-term goals

---

**💡 Tip:** Start with simple tasks and gradually complicate the process. The system adapts to your needs! 