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

"""Prompt Builder Sub-Agent - Creates detailed agent instructions/prompts."""

from google.adk.agents.llm_agent import LlmAgent
from ..prompts import PROMPT_BUILDER_PROMPT

prompt_builder = LlmAgent(
    name="prompt_builder",
    model="gemini-2.0-flash",
    description="""
    Prompt Engineering Specialist that creates detailed, effective instructions 
    for AI agents. Focuses on clear role definition, tool usage, response 
    guidelines, and error handling.
    """,
    instruction=PROMPT_BUILDER_PROMPT
) 