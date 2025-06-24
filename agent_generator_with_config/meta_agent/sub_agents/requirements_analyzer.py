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

"""Requirements Analyzer Sub-Agent - Analyzes user requirements for agent creation."""

from google.adk.agents.llm_agent import LlmAgent
from ..prompts import REQUIREMENTS_ANALYZER_PROMPT

requirements_analyzer = LlmAgent(
    name="requirements_analyzer",
    model="gemini-2.0-flash",
    description="""
    Requirements Analysis Specialist that extracts and structures user requirements 
    for agent creation. Analyzes user input to understand purpose, capabilities, 
    tools needed, and complexity level.
    """,
    instruction=REQUIREMENTS_ANALYZER_PROMPT
)