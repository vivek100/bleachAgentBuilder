# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Config Merger Tool - Manages agent configuration state throughout the creation process.
Provides comprehensive functions for creating, updating, and managing agent configurations.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# In-memory storage for configurations (in production, this could be a database)
_config_storage: Dict[str, Dict[str, Any]] = {}


def create_project(
    session_id: str,
    project_name: str,
    description: str = "",
    version: str = "1.0.0"
) -> str:
    """
    Create a new agent project configuration.
    
    Args:
        session_id: Unique session identifier
        project_name: Name of the project
        description: Project description
        version: Project version
        
    Returns:
        JSON string with project creation status
    """
    input_params = {
        "session_id": session_id,
        "project_name": project_name,
        "description": description,
        "version": version
    }
    
    try:
        config = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "project_config": {
                "project_name": project_name,
                "description": description,
                "version": version,
                "main_agent": "",
                "agents": {},
                "tools": {},
                "requirements": [],
                "environment_variables": {},
                "environment_variables_example": {}
            },
            "build_context": {
                "requirements_analysis": {},
                "architecture_plan": {},
                "agents_to_build": [],
                "tools_to_build": [],
                "current_agent_being_built": "",
                "current_tool_being_built": ""
            }
        }
        
        _config_storage[session_id] = config
        
        result = {
            "success": True,
            "message": f"Project '{project_name}' created successfully",
            "session_id": session_id,
            "project_name": project_name,
            "config_created": {
                "project_name": project_name,
                "description": description,
                "version": version,
                "main_agent": "",
                "agents_count": 0,
                "tools_count": 0
            }
        }
        
        return json.dumps({
            "tool": "create_project",
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to create project: {str(e)}"
        }
        
        return json.dumps({
            "tool": "create_project",
            "input": input_params,
            "result": error_result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)


def update_project_metadata(
    session_id: str,
    main_agent: Optional[str] = None,
    requirements: Optional[List[str]] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    environment_variables_example: Optional[Dict[str, str]] = None
) -> str:
    """
    Update project metadata.
    
    Args:
        session_id: Session identifier
        main_agent: Name of the main/root agent
        requirements: Python package requirements
        environment_variables: Environment variables with actual values
        environment_variables_example: Environment variables with example values
        
    Returns:
        JSON string with update status
    """
    input_params = {
        "session_id": session_id,
        "main_agent": main_agent,
        "requirements": requirements,
        "environment_variables": environment_variables,
        "environment_variables_example": environment_variables_example
    }
    
    try:
        if session_id not in _config_storage:
            error_result = {
                "success": False,
                "error": f"Session {session_id} not found"
            }
            return json.dumps({
                "tool": "update_project_metadata",
                "input": input_params,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            })
        
        config = _config_storage[session_id]
        changes = {}
        
        if main_agent:
            old_main_agent = config["project_config"]["main_agent"]
            config["project_config"]["main_agent"] = main_agent
            changes["main_agent"] = {"old": old_main_agent, "new": main_agent}
            
        if requirements:
            old_requirements = config["project_config"]["requirements"].copy()
            config["project_config"]["requirements"].extend(requirements)
            # Remove duplicates
            config["project_config"]["requirements"] = list(set(config["project_config"]["requirements"]))
            changes["requirements"] = {"old": old_requirements, "new": config["project_config"]["requirements"]}
            
        if environment_variables:
            old_env_vars = config["project_config"]["environment_variables"].copy()
            config["project_config"]["environment_variables"].update(environment_variables)
            changes["environment_variables"] = {"old": old_env_vars, "new": config["project_config"]["environment_variables"]}
            
        if environment_variables_example:
            old_env_vars_example = config["project_config"]["environment_variables_example"].copy()
            config["project_config"]["environment_variables_example"].update(environment_variables_example)
            changes["environment_variables_example"] = {"old": old_env_vars_example, "new": config["project_config"]["environment_variables_example"]}
        
        config["updated_at"] = datetime.now().isoformat()
        
        result = {
            "success": True,
            "message": "Project metadata updated successfully",
            "changes": changes,
            "updated_fields": {
                "main_agent": main_agent is not None,
                "requirements": requirements is not None,
                "environment_variables": environment_variables is not None,
                "environment_variables_example": environment_variables_example is not None
            },
            "current_config": {
                "project_name": config["project_config"]["project_name"],
                "main_agent": config["project_config"]["main_agent"],
                "requirements_count": len(config["project_config"]["requirements"]),
                "env_vars_count": len(config["project_config"]["environment_variables"])
            }
        }
        
        return json.dumps({
            "tool": "update_project_metadata",
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to update project metadata: {str(e)}"
        }
        
        return json.dumps({
            "tool": "update_project_metadata",
            "input": input_params,
            "result": error_result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)


def add_agent_to_config(
    session_id: str,
    agent_name: str,
    agent_type: str,
    description: str,
    model: Optional[str] = None,
    instruction: Optional[str] = None,
    tools: Optional[List[str]] = None,
    sub_agents: Optional[List[str]] = None,
    config_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Add a new agent to the project configuration.
    
    Args:
        session_id: Session identifier
        agent_name: Name of the agent
        agent_type: Type of agent (llm_agent, sequential_agent, etc.)
        description: Agent description
        model: LLM model to use (for LLM agents)
        instruction: Agent instructions/prompt
        tools: List of tool names the agent uses
        sub_agents: List of sub-agent names
        config_params: Additional configuration parameters
        
    Returns:
        JSON string with add status
    """
    input_params = {
        "session_id": session_id,
        "agent_name": agent_name,
        "agent_type": agent_type,
        "description": description,
        "model": model,
        "instruction": instruction,
        "tools": tools,
        "sub_agents": sub_agents,
        "config_params": config_params
    }
    
    try:
        if session_id not in _config_storage:
            error_result = {
                "success": False,
                "error": f"Session {session_id} not found"
            }
            return json.dumps({
                "tool": "add_agent_to_config",
                "input": input_params,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            })
        
        config = _config_storage[session_id]
        
        agent_config = {
            "name": agent_name,
            "type": agent_type,
            "description": description,
            "tools": tools or [],
            "sub_agents": sub_agents or [],
            "config": config_params or {}
        }
        
        # Add LLM-specific fields if it's an LLM agent
        if agent_type == "llm_agent":
            agent_config["model"] = model or "gemini-2.0-flash-lite-001"
            agent_config["instruction"] = instruction or "You are a helpful AI assistant."
        
        config["project_config"]["agents"][agent_name] = agent_config
        config["updated_at"] = datetime.now().isoformat()
        
        result = {
            "success": True,
            "message": f"Agent '{agent_name}' added successfully",
            "agent_added": agent_config,
            "total_agents": len(config["project_config"]["agents"]),
            "all_agents": list(config["project_config"]["agents"].keys())
        }
        
        return json.dumps({
            "tool": "add_agent_to_config",
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to add agent: {str(e)}"
        }
        
        return json.dumps({
            "tool": "add_agent_to_config",
            "input": input_params,
            "result": error_result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)


def update_agent_in_config(
    session_id: str,
    agent_name: str,
    description: Optional[str] = None,
    model: Optional[str] = None,
    instruction: Optional[str] = None,
    tools: Optional[List[str]] = None,
    sub_agents: Optional[List[str]] = None,
    config_params: Optional[Dict[str, Any]] = None
) -> str:
    """
    Update an existing agent in the configuration.
    
    Args:
        session_id: Session identifier
        agent_name: Name of the agent to update
        description: Updated description
        model: Updated model
        instruction: Updated instruction
        tools: Updated tools list
        sub_agents: Updated sub-agents list
        config_params: Updated configuration parameters
        
    Returns:
        JSON string with update status
    """
    input_params = {
        "session_id": session_id,
        "agent_name": agent_name,
        "description": description,
        "model": model,
        "instruction": instruction,
        "tools": tools,
        "sub_agents": sub_agents,
        "config_params": config_params
    }
    
    try:
        if session_id not in _config_storage:
            error_result = {
                "success": False,
                "error": f"Session {session_id} not found"
            }
            return json.dumps({
                "tool": "update_agent_in_config",
                "input": input_params,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            })
        
        config = _config_storage[session_id]
        
        if agent_name not in config["project_config"]["agents"]:
            error_result = {
                "success": False,
                "error": f"Agent '{agent_name}' not found"
            }
            return json.dumps({
                "tool": "update_agent_in_config",
                "input": input_params,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            })
        
        agent_config = config["project_config"]["agents"][agent_name]
        old_config = agent_config.copy()
        changes = {}
        
        # Update fields if provided
        if description:
            old_description = agent_config.get("description", "")
            agent_config["description"] = description
            changes["description"] = {"old": old_description, "new": description}
        if model and agent_config.get("type") == "llm_agent":
            old_model = agent_config.get("model", "")
            agent_config["model"] = model
            changes["model"] = {"old": old_model, "new": model}
        if instruction and agent_config.get("type") == "llm_agent":
            old_instruction = agent_config.get("instruction", "")
            agent_config["instruction"] = instruction
            changes["instruction"] = {"old": old_instruction, "new": instruction}
        if tools is not None:
            old_tools = agent_config.get("tools", [])
            agent_config["tools"] = tools
            changes["tools"] = {"old": old_tools, "new": tools}
        if sub_agents is not None:
            old_sub_agents = agent_config.get("sub_agents", [])
            agent_config["sub_agents"] = sub_agents
            changes["sub_agents"] = {"old": old_sub_agents, "new": sub_agents}
        if config_params:
            old_config_params = agent_config.get("config", {}).copy()
            agent_config["config"].update(config_params)
            changes["config_params"] = {"old": old_config_params, "new": agent_config["config"]}
        
        config["updated_at"] = datetime.now().isoformat()
        
        result = {
            "success": True,
            "message": f"Agent '{agent_name}' updated successfully",
            "agent_name": agent_name,
            "changes": changes,
            "updated_agent": agent_config
        }
        
        return json.dumps({
            "tool": "update_agent_in_config",
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to update agent: {str(e)}"
        }
        
        return json.dumps({
            "tool": "update_agent_in_config",
            "input": input_params,
            "result": error_result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)


def add_tool_to_config(
    session_id: str,
    tool_name: str,
    tool_type: str,
    description: str,
    builtin_type: Optional[str] = None,
    function_code: Optional[str] = None,
    imports: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None
) -> str:
    """
    Add a new tool to the project configuration.
    
    Args:
        session_id: Session identifier
        tool_name: Name of the tool
        tool_type: Type of tool (builtin or custom_function)
        description: Tool description
        builtin_type: Type of builtin tool (if tool_type is builtin)
        function_code: Python function code (if tool_type is custom_function)
        imports: Required imports for custom functions
        dependencies: Required Python packages
        
    Returns:
        JSON string with add status
    """
    input_params = {
        "session_id": session_id,
        "tool_name": tool_name,
        "tool_type": tool_type,
        "description": description,
        "builtin_type": builtin_type,
        "function_code": function_code,
        "imports": imports,
        "dependencies": dependencies
    }
    
    try:
        if session_id not in _config_storage:
            return json.dumps({
                "success": False,
                "error": f"Session {session_id} not found"
            })
        
        config = _config_storage[session_id]
        
        tool_config = {
            "name": tool_name,
            "type": tool_type,
            "description": description
        }
        
        if tool_type == "builtin":
            tool_config["builtin_type"] = builtin_type
        elif tool_type == "custom_function":
            tool_config["function_code"] = function_code
            if imports:
                tool_config["imports"] = imports
            if dependencies:
                tool_config["dependencies"] = dependencies
                # Add dependencies to project requirements
                config["project_config"]["requirements"].extend(dependencies)
                config["project_config"]["requirements"] = list(set(config["project_config"]["requirements"]))
        
        config["project_config"]["tools"][tool_name] = tool_config
        config["updated_at"] = datetime.now().isoformat()
        
        return json.dumps({
            "success": True,
            "message": f"Tool '{tool_name}' added successfully",
            "tool_name": tool_name,
            "tool_type": tool_type
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to add tool: {str(e)}"
        }, indent=2)


def update_tool_in_config(
    session_id: str,
    tool_name: str,
    description: Optional[str] = None,
    function_code: Optional[str] = None,
    imports: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None
) -> str:
    """
    Update an existing tool in the configuration.
    
    Args:
        session_id: Session identifier
        tool_name: Name of the tool to update
        description: Updated description
        function_code: Updated function code
        imports: Updated imports list
        dependencies: Updated dependencies list
        
    Returns:
        JSON string with update status
    """
    try:
        if session_id not in _config_storage:
            return json.dumps({
                "success": False,
                "error": f"Session {session_id} not found"
            })
        
        config = _config_storage[session_id]
        
        if tool_name not in config["project_config"]["tools"]:
            return json.dumps({
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            })
        
        tool_config = config["project_config"]["tools"][tool_name]
        
        # Update fields if provided
        if description:
            tool_config["description"] = description
        if function_code and tool_config.get("type") == "custom_function":
            tool_config["function_code"] = function_code
        if imports is not None and tool_config.get("type") == "custom_function":
            tool_config["imports"] = imports
        if dependencies is not None and tool_config.get("type") == "custom_function":
            tool_config["dependencies"] = dependencies
            # Update project requirements
            config["project_config"]["requirements"].extend(dependencies)
            config["project_config"]["requirements"] = list(set(config["project_config"]["requirements"]))
        
        config["updated_at"] = datetime.now().isoformat()
        
        return json.dumps({
            "success": True,
            "message": f"Tool '{tool_name}' updated successfully"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to update tool: {str(e)}"
        }, indent=2)


def get_full_config(session_id: str) -> str:
    """
    Get the complete configuration for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        JSON string with the full configuration
    """
    try:
        if session_id not in _config_storage:
            return json.dumps({
                "success": False,
                "error": f"Session {session_id} not found"
            })
        
        config = _config_storage[session_id]
        
        return json.dumps({
            "success": True,
            "config": config
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to get config: {str(e)}"
        }, indent=2)


def get_config_summary(session_id: str) -> str:
    """
    Get a summary of the current configuration state.
    
    Args:
        session_id: Session identifier
        
    Returns:
        JSON string with configuration summary
    """
    try:
        if session_id not in _config_storage:
            return json.dumps({
                "success": False,
                "error": f"Session {session_id} not found"
            })
        
        config = _config_storage[session_id]
        project_config = config["project_config"]
        
        summary = {
            "session_id": session_id,
            "project_name": project_config["project_name"],
            "main_agent": project_config["main_agent"],
            "agent_count": len(project_config["agents"]),
            "tool_count": len(project_config["tools"]),
            "agents": list(project_config["agents"].keys()),
            "tools": list(project_config["tools"].keys()),
            "requirements_count": len(project_config["requirements"]),
            "env_vars_count": len(project_config["environment_variables"]),
            "created_at": config["created_at"],
            "updated_at": config["updated_at"]
        }
        
        return json.dumps({
            "success": True,
            "summary": summary
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to get config summary: {str(e)}"
        }, indent=2)


def update_build_context(
    session_id: str,
    requirements_analysis: Optional[Dict] = None,
    architecture_plan: Optional[Dict] = None,
    agents_to_build: Optional[List[str]] = None,
    tools_to_build: Optional[List[str]] = None,
    current_agent_being_built: Optional[str] = None,
    current_tool_being_built: Optional[str] = None
) -> str:
    """
    Update the build context for tracking progress.
    
    Args:
        session_id: Session identifier
        requirements_analysis: Requirements analysis results
        architecture_plan: Architecture plan results
        agents_to_build: List of agents that need to be built
        tools_to_build: List of tools that need to be built
        current_agent_being_built: Current agent being processed
        current_tool_being_built: Current tool being processed
        
    Returns:
        JSON string with update status
    """
    try:
        if session_id not in _config_storage:
            return json.dumps({
                "success": False,
                "error": f"Session {session_id} not found"
            })
        
        config = _config_storage[session_id]
        build_context = config["build_context"]
        
        if requirements_analysis is not None:
            build_context["requirements_analysis"] = requirements_analysis
        if architecture_plan is not None:
            build_context["architecture_plan"] = architecture_plan
        if agents_to_build is not None:
            build_context["agents_to_build"] = agents_to_build
        if tools_to_build is not None:
            build_context["tools_to_build"] = tools_to_build
        if current_agent_being_built is not None:
            build_context["current_agent_being_built"] = current_agent_being_built
        if current_tool_being_built is not None:
            build_context["current_tool_being_built"] = current_tool_being_built
        
        config["updated_at"] = datetime.now().isoformat()
        
        return json.dumps({
            "success": True,
            "message": "Build context updated successfully"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to update build context: {str(e)}"
        }, indent=2)


def delete_session(session_id: str) -> str:
    """
    Delete a session and its configuration.
    
    Args:
        session_id: Session identifier
        
    Returns:
        JSON string with deletion status
    """
    try:
        if session_id not in _config_storage:
            return json.dumps({
                "success": False,
                "error": f"Session {session_id} not found"
            })
        
        del _config_storage[session_id]
        
        return json.dumps({
            "success": True,
            "message": f"Session {session_id} deleted successfully"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to delete session: {str(e)}"
        }, indent=2)


def list_sessions() -> str:
    """
    List all active sessions.
    
    Returns:
        JSON string with list of sessions
    """
    try:
        sessions = []
        for session_id, config in _config_storage.items():
            sessions.append({
                "session_id": session_id,
                "project_name": config["project_config"]["project_name"],
                "created_at": config["created_at"],
                "updated_at": config["updated_at"],
                "agent_count": len(config["project_config"]["agents"]),
                "tool_count": len(config["project_config"]["tools"])
            })
        
        return json.dumps({
            "success": True,
            "sessions": sessions
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to list sessions: {str(e)}"
        }, indent=2) 