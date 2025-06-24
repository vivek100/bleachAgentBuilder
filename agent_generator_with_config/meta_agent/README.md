# Agent Creator Meta-Agent

A sophisticated meta-agent system that creates other AI agents based on natural language descriptions. This system uses a multi-agent architecture to analyze requirements, design agent structures, and generate complete Python agent projects.

## 🏗️ Architecture

```
Agent Creator Orchestrator (Main Agent)
├── Requirements Analyzer - Extracts and structures user requirements
├── Architecture Planner - Designs agent system structure  
├── Agent Builder - Creates individual agent configurations
│   └── Prompt Builder - Creates detailed agent instructions
├── Tool Builder - Creates custom tools with Python code
└── Tools:
    ├── Config Merger - Manages configuration state
    └── Code Generator - Converts config to Python code
```

## 🚀 Features

- **Natural Language Input**: Describe your agent in plain English
- **Multi-Agent Creation**: Supports complex systems with multiple specialized agents
- **Custom Tool Generation**: Creates Python functions for specific needs
- **Comprehensive Output**: Generates complete agent projects with documentation
- **Session Management**: Tracks configuration state throughout the process
- **Validation & Error Handling**: Ensures generated agents are valid and functional

## 📋 Workflow

1. **Requirements Analysis** - Analyzes user description to extract purpose, capabilities, and complexity
2. **Architecture Planning** - Designs the agent structure and relationships
3. **Project Setup** - Initializes the configuration with project metadata
4. **Agent Building Loop** - For each agent:
   - Creates basic configuration
   - Generates detailed prompts/instructions
   - Adds to project configuration
5. **Tool Building Loop** - For each tool:
   - Creates custom Python functions or uses builtin tools
   - Adds to project configuration
6. **Code Generation** - Converts final configuration to Python files

## 🛠️ Usage

### Basic Usage

```python
from meta_agent import root_agent

# Describe your agent
user_request = """
Create a research assistant that can search the web, 
analyze web pages, and provide well-sourced answers.
"""

# Generate the agent
response = root_agent.run(user_request)
print(response)
```

### Command Line Usage

```bash
# Simple test
python main.py simple

# Complex multi-agent test  
python main.py complex

# Interactive mode
python main.py interactive
```

## 📁 Generated Output

The system generates complete agent projects with:

- `agent.py` - Main agent implementation
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `.env.example` - Environment variable template
- `quick_start.py` - Quick start script
- `generation_summary.json` - Generation metadata

## 🔧 Configuration Tools

### Config Merger Functions

- `create_project()` - Initialize new project
- `add_agent_to_config()` - Add agent to configuration
- `add_tool_to_config()` - Add tool to configuration
- `update_agent_in_config()` - Modify existing agent
- `update_tool_in_config()` - Modify existing tool
- `get_full_config()` - Retrieve complete configuration
- `get_config_summary()` - Get configuration overview

### Code Generator Functions

- `generate_agent_code()` - Convert config to Python code
- `preview_generated_code()` - Preview without writing files
- `validate_configuration()` - Check config validity

## 📊 Supported Agent Types

- **LLM Agent** - Single AI agent with tools and prompts
- **Sequential Agent** - Runs sub-agents in sequence
- **Parallel Agent** - Runs sub-agents simultaneously
- **Loop Agent** - Runs sub-agent in a loop until condition met

## 🔨 Supported Tools

### Builtin Tools
- `google_search` - Web search capabilities
- `url_context` - Load and analyze web pages
- `load_memory` - Access stored memories
- `preload_memory` - Load specific memories
- `load_artifacts` - Access saved artifacts
- `transfer_to_agent` - Call other agents
- `get_user_choice` - User interaction
- `exit_loop` - Loop control

### Custom Tools
- Python functions with proper error handling
- Custom imports and dependencies
- Integration with external APIs and services

## 🎯 Example Scenarios

### Simple Research Agent
```
"Create a research assistant that searches the web and analyzes content."
```

### E-commerce Customer Service
```
"Create a customer service system with intent classification, 
product specialist, order tracking, and human escalation."
```

### Data Processing Pipeline
```
"Create a data processing system that fetches data from APIs, 
processes it with pandas, and generates reports."
```

## 🔍 Session Management

Each agent creation process gets a unique session ID that tracks:
- Requirements analysis results
- Architecture plan
- Current configuration state
- Build context and progress
- Generated code and files

Sessions persist throughout the creation process and can be referenced for modifications or regeneration.

## ⚙️ Configuration Schema

The system uses a comprehensive JSON schema based on the existing config generator:

```json
{
  "project_name": "string",
  "description": "string", 
  "version": "string",
  "main_agent": "string",
  "agents": {
    "agent_name": {
      "name": "string",
      "type": "llm_agent|sequential_agent|parallel_agent|loop_agent",
      "description": "string",
      "model": "string",
      "instruction": "string",
      "tools": ["tool_names"],
      "sub_agents": ["sub_agent_names"],
      "config": {}
    }
  },
  "tools": {
    "tool_name": {
      "name": "string",
      "type": "builtin|custom_function",
      "description": "string",
      "function_code": "string",
      "imports": ["import_statements"],
      "dependencies": ["packages"]
    }
  },
  "requirements": ["packages"],
  "environment_variables": {}
}
```

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Run a test:
   ```bash
   python main.py simple
   ```

4. Try interactive mode:
   ```bash
   python main.py interactive
   ```

## 🤝 Integration

The meta-agent can be integrated into:
- Web applications via REST API
- Command-line tools
- Jupyter notebooks for experimentation
- Larger agent systems as a specialized component

## 📈 Future Enhancements

- Database persistence for session management
- Web UI for visual agent design
- Agent testing and validation tools
- Integration with more ADK features
- Template-based agent creation
- Version control for agent configurations

## 🔧 Development

The system is built using:
- **Google ADK** - Agent Development Kit
- **Pydantic** - Data validation and settings
- **JSON Schema** - Configuration validation  
- **Modular Architecture** - Clean separation of concerns

Each component is independently testable and can be extended or modified without affecting others.

---

*Generated by ADK Agent Generator Meta-Agent v1.0.0* 