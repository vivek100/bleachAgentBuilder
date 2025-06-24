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
JSON Schema definitions for ADK Agent Configuration.
Based on analysis of existing ADK agents, tools, and planners.
"""

from typing import Dict, List, Optional, Union, Any, Literal
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class AgentType(str, Enum):
    """Available agent types in ADK."""
    LLM_AGENT = "llm_agent"
    SEQUENTIAL_AGENT = "sequential_agent"
    PARALLEL_AGENT = "parallel_agent"
    LOOP_AGENT = "loop_agent"


class BuiltinToolType(str, Enum):
    """Available builtin tools in ADK."""
    GOOGLE_SEARCH = "google_search"
    URL_CONTEXT = "url_context"
    LOAD_MEMORY = "load_memory"
    PRELOAD_MEMORY = "preload_memory"
    LOAD_ARTIFACTS = "load_artifacts"
    TRANSFER_TO_AGENT = "transfer_to_agent"
    GET_USER_CHOICE = "get_user_choice"
    EXIT_LOOP = "exit_loop"


class ToolConfig(BaseModel):
    """Configuration for a tool."""
    model_config = ConfigDict(extra="forbid", exclude_none=True)
    
    name: str = Field(..., description="Name of the tool")
    type: Literal["builtin", "custom_function"] = Field(..., description="Type of tool")
    description: str = Field(..., description="Description of what the tool does")
    
    # For builtin tools
    builtin_type: Optional[BuiltinToolType] = Field(default=None, description="Type of builtin tool")
    
    # For custom function tools
    function_code: Optional[str] = Field(default=None, description="Python function code for custom tools")
    imports: Optional[List[str]] = Field(default=None, description="Additional imports needed for custom function (e.g., ['import json', 'from datetime import datetime'])")
    dependencies: Optional[List[str]] = Field(default=None, description="Additional Python packages required (e.g., ['requests', 'pandas'])")


class AgentConfig(BaseModel):
    """Configuration for a single agent."""
    model_config = ConfigDict(extra="forbid", exclude_none=True)
    
    name: str = Field(..., description="Agent name (must be Python identifier)")
    type: AgentType = Field(..., description="Type of agent")
    description: str = Field(..., description="Agent description")
    
    # LLM-specific fields
    model: Optional[str] = Field(default=None, description="LLM model to use")
    instruction: Optional[str] = Field(default=None, description="Agent instructions/prompt")
    
    # Tools and sub-agents
    tools: List[str] = Field(default_factory=list, description="List of tool names this agent uses")
    sub_agents: List[str] = Field(default_factory=list, description="List of sub-agent names")
    
    # Configuration options
    config: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific configuration")


class AgentProjectConfig(BaseModel):
    """Complete agent project configuration."""
    model_config = ConfigDict(extra="forbid", exclude_none=True)
    
    project_name: str = Field(..., description="Name of the agent project")
    description: str = Field(default="", description="Project description")
    version: str = Field(default="1.0.0", description="Project version")
    
    # Main entry point
    main_agent: str = Field(..., description="Name of the main/root agent")
    
    # Components
    agents: Dict[str, AgentConfig] = Field(..., description="Agent definitions")
    tools: Dict[str, ToolConfig] = Field(default_factory=dict, description="Tool definitions")
    
    # Project metadata
    requirements: List[str] = Field(default_factory=list, description="Python dependencies")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables with actual values (will be written to .env file)")
    environment_variables_example: Dict[str, str] = Field(default_factory=dict, description="Environment variables with example/placeholder values (will be written to .env.example file)")


# Validation functions
def validate_agent_config(config: AgentProjectConfig) -> List[str]:
    """Validate agent configuration and return list of errors."""
    errors = []
    
    # Check main agent exists
    if config.main_agent not in config.agents:
        errors.append(f"Main agent '{config.main_agent}' not found in agents")
    
    # Check all referenced sub-agents exist
    for agent_name, agent in config.agents.items():
        for sub_agent in agent.sub_agents:
            if sub_agent not in config.agents:
                errors.append(f"Sub-agent '{sub_agent}' referenced by '{agent_name}' not found")
    
    # Check all referenced tools exist
    for agent_name, agent in config.agents.items():
        for tool_name in agent.tools:
            if tool_name not in config.tools:
                errors.append(f"Tool '{tool_name}' referenced by '{agent_name}' not found")
    
    # Validate agent types have required fields
    for agent_name, agent in config.agents.items():
        if agent.type == AgentType.LLM_AGENT:
            if not agent.model:
                errors.append(f"LLM agent '{agent_name}' missing required 'model' field")
            if not agent.instruction:
                errors.append(f"LLM agent '{agent_name}' missing required 'instruction' field")
        
        # Sequential/Parallel/Loop agents need sub-agents
        if agent.type in [AgentType.SEQUENTIAL_AGENT, AgentType.PARALLEL_AGENT, AgentType.LOOP_AGENT]:
            if not agent.sub_agents:
                errors.append(f"{agent.type} agent '{agent_name}' needs at least one sub-agent")
    
    # Validate tool configurations
    for tool_name, tool in config.tools.items():
        if tool.type == "builtin" and not tool.builtin_type:
            errors.append(f"Builtin tool '{tool_name}' missing builtin_type")
        if tool.type == "custom_function" and not tool.function_code:
            errors.append(f"Custom tool '{tool_name}' missing function_code")
    
    return errors


def get_default_model() -> str:
    """Get default model from environment or fallback."""
    import os
    return os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-lite-001") 