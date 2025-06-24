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

"""Configuration module for the agent creator meta-agent."""

import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentModel(BaseModel):
    """Agent model settings."""
    
    name: str = Field(default="agent_creator_orchestrator")
    model: str = Field(default="gemini-2.0-flash")


class Config(BaseSettings):
    """Configuration settings for the agent creator meta-agent."""
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../.env"
        ),
        env_prefix="AGENT_CREATOR_",
        case_sensitive=True,
        extra="allow"  # Allow extra environment variables
    )
    
    agent_settings: AgentModel = Field(default=AgentModel())
    app_name: str = "agent_creator_app"
    
    # Generation settings
    OUTPUT_BASE_DIR: str = Field(default="./generated_agents")
    SESSION_TIMEOUT_MINUTES: int = Field(default=30)
    MAX_AGENTS_PER_PROJECT: int = Field(default=10)
    MAX_TOOLS_PER_PROJECT: int = Field(default=20)
    
    # Cloud settings (optional)
    CLOUD_PROJECT: str = Field(default="")
    CLOUD_LOCATION: str = Field(default="us-central1")
    GENAI_USE_VERTEXAI: str = Field(default="0")
    API_KEY: str | None = Field(default="")
    
    # Common Google/ADK environment variables (to avoid validation errors)
    GOOGLE_API_KEY: str | None = Field(default="")
    GOOGLE_SEARCH_ENGINE_ID: str | None = Field(default="")
    GOOGLE_CLOUD_PROJECT: str | None = Field(default="")
    GOOGLE_GENAI_USE_VERTEXAI: str | None = Field(default="") 