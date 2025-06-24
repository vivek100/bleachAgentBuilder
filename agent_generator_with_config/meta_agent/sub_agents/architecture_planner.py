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

"""Architecture Planner Sub-Agent - Designs agent system structure."""

from google.adk.agents.llm_agent import LlmAgent
from ..prompts import ARCHITECTURE_PLANNER_PROMPT

architecture_planner = LlmAgent(
    name="architecture_planner",
    model="gemini-2.0-flash-lite-001",
    description="""
    Agent Architecture Specialist that designs the structure of agent systems.
    Creates simple, clear architecture plans defining agents, their roles, 
    and relationships without complex data flow design.
    """,
    instruction=ARCHITECTURE_PLANNER_PROMPT
) 