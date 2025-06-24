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
Agent Creator Meta-Agent - Creates other agents based on user requirements.
This agent orchestrates the creation of agent configurations and generates code.
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool

from .config import Config
from .prompts import ORCHESTRATOR_PROMPT
from .sub_agents.requirements_analyzer import requirements_analyzer
from .sub_agents.architecture_planner import architecture_planner  
from .sub_agents.agent_builder import agent_builder
from .sub_agents.tool_builder import tool_builder
from .tools.config_merger import (
    create_project,
    update_project_metadata,
    add_agent_to_config,
    update_agent_in_config,
    add_tool_to_config,
    update_tool_in_config,
    get_full_config,
    get_config_summary
)
from .tools.code_generator import generate_agent_code

configs = Config()

# Main orchestrator agent
agent_creator_orchestrator = LlmAgent(
    name="agent_creator_orchestrator",
    model=configs.agent_settings.model,
    description="""
    Main orchestrator for creating agent configurations. Manages the workflow:
    analyze requirements → plan architecture → build each agent → build tools → generate code.
    Passes the evolving config object through the pipeline and manages session state.
    """,
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        # Sub-agents as tools
        AgentTool(agent=requirements_analyzer),
        AgentTool(agent=architecture_planner),
        AgentTool(agent=agent_builder),
        AgentTool(agent=tool_builder),
        
        # Config management tools
        FunctionTool(create_project),
        FunctionTool(update_project_metadata),
        FunctionTool(add_agent_to_config),
        FunctionTool(update_agent_in_config),
        FunctionTool(add_tool_to_config),
        FunctionTool(update_tool_in_config),
        FunctionTool(get_full_config),
        FunctionTool(get_config_summary),
        
        # Code generation tool
        FunctionTool(generate_agent_code)
    ]
)

# Main entry point
root_agent = agent_creator_orchestrator 