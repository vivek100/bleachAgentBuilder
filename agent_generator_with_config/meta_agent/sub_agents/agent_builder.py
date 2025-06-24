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

"""Agent Builder Sub-Agent - Builds individual agent configurations."""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool

from ..prompts import AGENT_BUILDER_PROMPT
from .prompt_builder import prompt_builder
from ..tools.config_merger import add_agent_to_config, update_agent_in_config

agent_builder = LlmAgent(
    name="agent_builder",
    model="gemini-2.0-flash",
    description="""
    Agent Configuration Specialist that builds detailed configurations for 
    individual agents. Creates basic agent config, calls prompt builder for 
    instructions, then merges everything using config_merger tools.
    """,
    instruction=AGENT_BUILDER_PROMPT,
    tools=[
        AgentTool(agent=prompt_builder),
        FunctionTool(add_agent_to_config),
        FunctionTool(update_agent_in_config)
    ]
) 