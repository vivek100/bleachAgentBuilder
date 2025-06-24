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

"""Tool Builder Sub-Agent - Creates custom tools with Python code."""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.function_tool import FunctionTool

from ..prompts import TOOL_BUILDER_PROMPT
from ..tools.config_merger import add_tool_to_config, update_tool_in_config

tool_builder = LlmAgent(
    name="tool_builder",
    model="gemini-2.0-flash",
    description="""
    Tool Creation Specialist that creates custom tools with Python function code.
    Writes clean, functional Python code with proper error handling and adds 
    tools to the project configuration.
    """,
    instruction=TOOL_BUILDER_PROMPT,
    tools=[
        FunctionTool(add_tool_to_config),
        FunctionTool(update_tool_in_config)
    ]
) 