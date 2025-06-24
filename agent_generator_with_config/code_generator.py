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
Deterministic Config-to-Code Generator for ADK Agents.
Converts JSON configuration to Python agent code files.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set
try:
    from .config_schema import AgentProjectConfig, AgentConfig, ToolConfig, AgentType, BuiltinToolType
except ImportError:
    from config_schema import AgentProjectConfig, AgentConfig, ToolConfig, AgentType, BuiltinToolType


class AgentCodeGenerator:
    """Generates Python agent code from configuration."""
    
    def __init__(self):
        self.builtin_tool_imports = {
            BuiltinToolType.GOOGLE_SEARCH: "from google.adk.tools import google_search",
            BuiltinToolType.URL_CONTEXT: "from google.adk.tools import url_context", 
            BuiltinToolType.LOAD_MEMORY: "from google.adk.tools import load_memory",
            BuiltinToolType.PRELOAD_MEMORY: "from google.adk.tools import preload_memory",
            BuiltinToolType.LOAD_ARTIFACTS: "from google.adk.tools import load_artifacts",
            BuiltinToolType.TRANSFER_TO_AGENT: "from google.adk.tools import transfer_to_agent",
            BuiltinToolType.GET_USER_CHOICE: "from google.adk.tools import get_user_choice",
            BuiltinToolType.EXIT_LOOP: "from google.adk.tools import exit_loop",
        }
        
        self.builtin_tool_names = {
            BuiltinToolType.GOOGLE_SEARCH: "google_search",
            BuiltinToolType.URL_CONTEXT: "url_context",
            BuiltinToolType.LOAD_MEMORY: "load_memory", 
            BuiltinToolType.PRELOAD_MEMORY: "preload_memory",
            BuiltinToolType.LOAD_ARTIFACTS: "load_artifacts",
            BuiltinToolType.TRANSFER_TO_AGENT: "transfer_to_agent",
            BuiltinToolType.GET_USER_CHOICE: "get_user_choice",
            BuiltinToolType.EXIT_LOOP: "exit_loop",
        }
    
    def generate_from_config(self, config: AgentProjectConfig, output_dir: str = None) -> Dict[str, str]:
        """
        Generate Python code files from agent configuration.
        
        Args:
            config: The agent project configuration
            output_dir: Optional directory to write files to
            
        Returns:
            Dictionary mapping filename to file content
        """
        files = {}
        
        # Generate main agent.py file
        files["agent.py"] = self._generate_agent_file(config)
        
        # Generate __init__.py
        files["__init__.py"] = self._generate_init_file()
        
        # Generate requirements.txt
        files["requirements.txt"] = self._generate_requirements_file(config)
        
        # Generate README.md
        files["README.md"] = self._generate_readme_file(config)
        
        # Generate .env files if environment variables are specified
        if config.environment_variables or config.environment_variables_example:
            files[".env.example"] = self._generate_env_example_file(config)
        
        # Generate .env file with actual values if provided, for now create a .env.example file
        # as it messes with the testing as we have main env file at parent folder level
        ##if config.environment_variables:
        ##    files[".env"] = self._generate_env_file(config)
        
        # Write files to disk if output_dir is specified
        if output_dir:
            self._write_files_to_disk(files, output_dir)
        
        return files
    
    def _generate_agent_file(self, config: AgentProjectConfig) -> str:
        """Generate the main agent.py file."""
        
        # Collect imports
        imports = self._collect_imports(config)
        
        # Generate custom function tools
        custom_functions = self._generate_custom_functions(config)
        
        # Generate agent definitions (in dependency order)
        agent_definitions = self._generate_agent_definitions(config)
        
        # Combine into final file
        content = f"""# Copyright 2025 Google LLC
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

\"\"\"
{config.project_name}: {config.description}
Generated by ADK Agent Generator
\"\"\"

{chr(10).join(imports)}


{custom_functions}

{agent_definitions}

# Main agent (entry point)
root_agent = {config.main_agent}
"""
        return content
    
    def _collect_imports(self, config: AgentProjectConfig) -> List[str]:
        """Collect all necessary imports."""
        imports = set()
        
        # Base imports
        imports.add("from google.adk.agents.llm_agent import LlmAgent")
        imports.add("from google.adk.agents.sequential_agent import SequentialAgent") 
        imports.add("from google.adk.agents.parallel_agent import ParallelAgent")
        imports.add("from google.adk.agents.loop_agent import LoopAgent")
        imports.add("from google.adk.tools.function_tool import FunctionTool")
        imports.add("from google.genai import types")
        
        # Add typing imports if we have custom functions
        has_custom_functions = any(
            tool.type == "custom_function" for tool in config.tools.values()
        )
        if has_custom_functions:
            imports.add("from typing import List, Dict, Any, Optional")
        
        # Collect custom tool imports
        for tool in config.tools.values():
            if tool.type == "custom_function" and tool.imports:
                for import_stmt in tool.imports:
                    imports.add(import_stmt.strip())
        
        # Collect builtin tool imports
        for tool in config.tools.values():
            if tool.type == "builtin" and tool.builtin_type:
                import_stmt = self.builtin_tool_imports.get(tool.builtin_type)
                if import_stmt:
                    imports.add(import_stmt)
        
        return sorted(list(imports))
    
    def _generate_custom_functions(self, config: AgentProjectConfig) -> str:
        """Generate custom function definitions."""
        custom_functions = []
        
        for tool_name, tool in config.tools.items():
            if tool.type == "custom_function" and tool.function_code:
                # Ensure proper indentation and formatting
                function_code = tool.function_code.strip()
                custom_functions.append(f"# Tool: {tool.description}")
                custom_functions.append(function_code)
                custom_functions.append("")  # Empty line separator
        
        return "\n".join(custom_functions)
    
    def _generate_agent_definitions(self, config: AgentProjectConfig) -> str:
        """Generate agent definitions in dependency order."""
        agent_definitions = []
        
        # Sort agents by dependency (sub-agents first)
        sorted_agents = self._sort_agents_by_dependency(config)
        
        for agent_name in sorted_agents:
            agent = config.agents[agent_name]
            agent_code = self._generate_single_agent(agent_name, agent, config)
            agent_definitions.append(agent_code)
            agent_definitions.append("")  # Empty line separator
        
        return "\n".join(agent_definitions)
    
    def _sort_agents_by_dependency(self, config: AgentProjectConfig) -> List[str]:
        """Sort agents so sub-agents are defined before their parents."""
        sorted_agents = []
        remaining = set(config.agents.keys())
        
        while remaining:
            # Find agents with no unresolved dependencies
            ready = []
            for agent_name in remaining:
                agent = config.agents[agent_name]
                if all(sub_agent in sorted_agents for sub_agent in agent.sub_agents):
                    ready.append(agent_name)
            
            if not ready:
                # Circular dependency or other issue - just add remaining in arbitrary order
                ready = list(remaining)
            
            # Add ready agents
            for agent_name in ready:
                sorted_agents.append(agent_name)
                remaining.remove(agent_name)
        
        return sorted_agents
    
    def _generate_single_agent(self, agent_name: str, agent: AgentConfig, config: AgentProjectConfig) -> str:
        """Generate code for a single agent."""
        
        if agent.type == AgentType.LLM_AGENT:
            return self._generate_llm_agent(agent_name, agent, config)
        elif agent.type == AgentType.SEQUENTIAL_AGENT:
            return self._generate_sequential_agent(agent_name, agent, config)
        elif agent.type == AgentType.PARALLEL_AGENT:
            return self._generate_parallel_agent(agent_name, agent, config)
        elif agent.type == AgentType.LOOP_AGENT:
            return self._generate_loop_agent(agent_name, agent, config)
        else:
            raise ValueError(f"Unknown agent type: {agent.type}")
    
    def _generate_llm_agent(self, agent_name: str, agent: AgentConfig, config: AgentProjectConfig) -> str:
        """Generate LLM agent code."""
        
        # Build tools list
        tools_list = self._build_tools_list(agent.tools, config)
        
        # Build sub-agents list
        sub_agents_list = ", ".join(agent.sub_agents) if agent.sub_agents else None
        
        # Build configuration
        agent_config = self._build_agent_config(agent)
        
        code = f"""# {agent.description}
{agent_name} = LlmAgent(
    name="{agent_name}",
    model="{agent.model or 'gemini-2.0-flash-lite-001'}",
    description=\"\"\"
    {agent.description}
    \"\"\",
    instruction=\"\"\"
    {agent.instruction or 'You are a helpful AI assistant.'}
    \"\"\""""
        
        if tools_list:
            code += f",\n    tools=[{tools_list}]"
        
        if sub_agents_list:
            code += f",\n    sub_agents=[{sub_agents_list}]"
        
        if agent_config:
            code += f",\n{agent_config}"
        
        code += "\n)"
        
        return code
    
    def _generate_sequential_agent(self, agent_name: str, agent: AgentConfig, config: AgentProjectConfig) -> str:
        """Generate Sequential agent code."""
        sub_agents_list = ", ".join(agent.sub_agents)
        
        return f"""# {agent.description}
{agent_name} = SequentialAgent(
    name="{agent_name}",
    description=\"\"\"
    {agent.description}
    \"\"\",
    sub_agents=[{sub_agents_list}]
)"""
    
    def _generate_parallel_agent(self, agent_name: str, agent: AgentConfig, config: AgentProjectConfig) -> str:
        """Generate Parallel agent code."""
        sub_agents_list = ", ".join(agent.sub_agents)
        
        return f"""# {agent.description}
{agent_name} = ParallelAgent(
    name="{agent_name}",
    description=\"\"\"
    {agent.description}
    \"\"\",
    sub_agents=[{sub_agents_list}]
)"""
    

    
    def _generate_loop_agent(self, agent_name: str, agent: AgentConfig, config: AgentProjectConfig) -> str:
        """Generate Loop agent code."""
        sub_agent = agent.sub_agents[0] if agent.sub_agents else "None"
        
        return f"""# {agent.description}
{agent_name} = LoopAgent(
    name="{agent_name}",
    description=\"\"\"
    {agent.description}
    \"\"\",
    sub_agents=[{sub_agent}]
)"""
    
    def _build_tools_list(self, tool_names: List[str], config: AgentProjectConfig) -> str:
        """Build the tools list for an agent."""
        tools = []
        
        for tool_name in tool_names:
            tool = config.tools.get(tool_name)
            if not tool:
                continue
            
            if tool.type == "builtin" and tool.builtin_type:
                builtin_name = self.builtin_tool_names.get(tool.builtin_type)
                if builtin_name:
                    tools.append(builtin_name)
            elif tool.type == "custom_function":
                tools.append(f"FunctionTool({tool_name})")
        
        return ", ".join(tools)
    
    def _build_agent_config(self, agent: AgentConfig) -> str:
        """Build agent configuration parameters."""
        config_parts = []
        
        # Add common config options
        if agent.config.get("temperature") is not None:
            temp = agent.config["temperature"]
            config_parts.append(f'    generate_content_config=types.GenerateContentConfig(temperature={temp})')
        
        if agent.config.get("disallow_transfer_to_parent"):
            config_parts.append("    disallow_transfer_to_parent=True")
        
        if agent.config.get("disallow_transfer_to_peers"):
            config_parts.append("    disallow_transfer_to_peers=True")
        
        if agent.config.get("output_key"):
            output_key = agent.config["output_key"]
            config_parts.append(f'    output_key="{output_key}"')
        
        return ",\n".join(config_parts)
    
    def _generate_init_file(self) -> str:
        """Generate __init__.py file."""
        return """# Copyright 2025 Google LLC
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

# Generated agent package
"""
    
    def _generate_requirements_file(self, config: AgentProjectConfig) -> str:
        """Generate requirements.txt file."""
        requirements = set([
            "google-adk>=1.0.0",
        ])
        
        # Add any custom requirements
        requirements.update(config.requirements)
        
        # Add custom tool dependencies
        for tool in config.tools.values():
            if tool.type == "custom_function" and tool.dependencies:
                requirements.update(tool.dependencies)
        
        return "\n".join(sorted(requirements))
    
    def _generate_readme_file(self, config: AgentProjectConfig) -> str:
        """Generate README.md file."""
        return f"""# {config.project_name.title()}

{config.description}

## Overview

This agent was automatically generated using the ADK Agent Generator.

**Main Agent**: {config.main_agent}
**Version**: {config.version}

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (if any):
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. Run the agent:
   ```bash
   adk cli agent.py
   ```

## Architecture

### Agents
{self._generate_agent_docs(config)}

### Tools
{self._generate_tool_docs(config)}

## Generated by ADK Agent Generator v{config.version}
"""
    
    def _generate_agent_docs(self, config: AgentProjectConfig) -> str:
        """Generate agent documentation for README."""
        docs = []
        for agent_name, agent in config.agents.items():
            docs.append(f"- **{agent_name}** ({agent.type}): {agent.description}")
        return "\n".join(docs)
    
    def _generate_tool_docs(self, config: AgentProjectConfig) -> str:
        """Generate tool documentation for README."""
        docs = []
        for tool_name, tool in config.tools.items():
            docs.append(f"- **{tool_name}** ({tool.type}): {tool.description}")
        return "\n".join(docs)
    
    def _generate_env_example_file(self, config: AgentProjectConfig) -> str:
        """Generate .env.example file."""
        lines = ["# Environment variables for the agent"]
        lines.append("# Copy this file to .env and fill in actual values")
        lines.append("")
        
        # Use example values if provided, otherwise use placeholder
        env_vars = config.environment_variables_example or config.environment_variables
        for key, value in env_vars.items():
            lines.append(f"{key}={value}")
        return "\n".join(lines)
    
    def _generate_env_file(self, config: AgentProjectConfig) -> str:
        """Generate .env file with actual values."""
        lines = ["# Environment variables for the agent"]
        lines.append("")
        for key, value in config.environment_variables.items():
            lines.append(f"{key}={value}")
        return "\n".join(lines)
    
    def _write_files_to_disk(self, files: Dict[str, str], output_dir: str):
        """Write generated files to disk."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for filename, content in files.items():
            file_path = output_path / filename
            file_path.write_text(content, encoding='utf-8')
            print(f"Generated: {file_path}")


def generate_agent_from_config_file(config_file: str, output_dir: str = None) -> Dict[str, str]:
    """
    Generate agent code from a JSON configuration file.
    
    Args:
        config_file: Path to JSON configuration file
        output_dir: Optional output directory
        
    Returns:
        Dictionary mapping filename to file content
    """
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    config = AgentProjectConfig(**config_data)
    generator = AgentCodeGenerator()
    return generator.generate_from_config(config, output_dir)


def generate_agent_from_dict(config_dict: dict, output_dir: str = None) -> Dict[str, str]:
    """
    Generate agent code from a configuration dictionary.
    
    Args:
        config_dict: Configuration dictionary
        output_dir: Optional output directory
        
    Returns:
        Dictionary mapping filename to file content
    """
    config = AgentProjectConfig(**config_dict)
    generator = AgentCodeGenerator()
    return generator.generate_from_config(config, output_dir) 