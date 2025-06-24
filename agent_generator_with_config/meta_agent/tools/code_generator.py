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
Code Generator Tool - Converts final agent configuration to Python code files.
Uses the same AgentCodeGenerator class as the main code generator for consistency.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Import the AgentCodeGenerator class and related schemas
try:
    # Try relative import first
    from ...code_generator import AgentCodeGenerator
    from ...config_schema import validate_agent_config, AgentProjectConfig
except ImportError:
    try:
        # Try absolute import
        import sys
        import os
        from pathlib import Path
        
        # Add the parent directory to path
        parent_dir = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(parent_dir))
        
        from code_generator import AgentCodeGenerator
        from config_schema import validate_agent_config, AgentProjectConfig
    except ImportError as e:
        print(f"Warning: Could not import code generator: {e}")
        print("Make sure you're running from the correct directory")
        raise

from .config_merger import get_full_config


def generate_agent_code(
    session_id: str,
    output_base_dir: str = ".",
    validate_config: bool = True
) -> str:
    """
    Generate Python code files from the final agent configuration.
    Uses the same AgentCodeGenerator class as the main code generator for consistency.
    
    Args:
        session_id: Session identifier containing the configuration
        output_base_dir: Base directory for generated code (defaults to current directory)
        validate_config: Whether to validate the configuration before generation
        
    Returns:
        JSON string with generation results
    """
    input_params = {
        "session_id": session_id,
        "output_base_dir": output_base_dir,
        "validate_config": validate_config
    }
    
    try:
        # Get the full configuration
        config_response = get_full_config(session_id)
        config_data = json.loads(config_response)
        
        if not config_data.get("success"):
            return json.dumps({
                "success": False,
                "error": f"Failed to get configuration: {config_data.get('error', 'Unknown error')}"
            }, indent=2)
        
        # Extract the project configuration
        full_config = config_data["config"]
        project_config = full_config["project_config"]
        
        # Create AgentProjectConfig object
        try:
            config_obj = AgentProjectConfig(**project_config)
        except Exception as config_error:
            return json.dumps({
                "success": False,
                "error": f"Configuration parsing error: {str(config_error)}"
            }, indent=2)
        
        # Validate the configuration if requested
        if validate_config:
            try:
                validation_errors = validate_agent_config(config_obj)
                if validation_errors:
                    return json.dumps({
                        "success": False,
                        "error": "Configuration validation failed",
                        "validation_errors": validation_errors
                    }, indent=2)
            except Exception as validation_error:
                return json.dumps({
                    "success": False,
                    "error": f"Configuration validation error: {str(validation_error)}"
                }, indent=2)
        
        # Create output directory - generate directly in the current folder for easy testing
        project_name = project_config["project_name"]
        output_dir = Path(output_base_dir).resolve()
        
        # Ensure the directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate the code using the same AgentCodeGenerator class
        generator = AgentCodeGenerator()
        generated_files = generator.generate_from_config(config_obj, str(output_dir))
        
        # Create a summary file
        summary = {
            "session_id": session_id,
            "project_name": project_name,
            "generated_at": datetime.now().isoformat(),
            "output_directory": str(output_dir),
            "generated_files": list(generated_files.keys()),
            "agent_count": len(project_config["agents"]),
            "tool_count": len(project_config["tools"]),
            "main_agent": project_config["main_agent"],
            "agents": list(project_config["agents"].keys()),
            "tools": list(project_config["tools"].keys())
        }
        
        # Write summary file
        summary_path = output_dir / "generation_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save the project configuration for reference and regeneration
        config_path = output_dir / "project_config.json"
        with open(config_path, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        # Create a quick start script
        quick_start_content = f"""#!/usr/bin/env python3
# Quick start script for {project_name}

from agent import root_agent

def main():
    print("Starting {project_name}...")
    print("Main agent: {project_config['main_agent']}")
    print("Available agents: {list(project_config['agents'].keys())}")
    print("Available tools: {list(project_config['tools'].keys())}")
    print()
    print("Generated in current directory for easy testing with ADK Web UI")
    print()
    print("To run the agent with ADK CLI:")
    print("adk cli agent.py")
    print()
    print("To use the agent programmatically:")
    print("response = root_agent.run('Your message here')")
    print("print(response)")

if __name__ == "__main__":
    main()
"""
        
        quick_start_path = output_dir / "quick_start.py"
        with open(quick_start_path, 'w') as f:
            f.write(quick_start_content)
        
        # Make quick start script executable
        os.chmod(quick_start_path, 0o755)
        
        result = {
            "success": True,
            "message": f"Agent code generated successfully for project '{project_name}' using AgentCodeGenerator",
            "output_directory": str(output_dir),
            "generated_files": list(generated_files.keys()) + ["generation_summary.json", "project_config.json", "quick_start.py"],
            "summary": summary,
            "project_config": project_config
        }
        
        return json.dumps({
            "tool": "generate_agent_code",
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to generate agent code: {str(e)}"
        }
        
        return json.dumps({
            "tool": "generate_agent_code",
            "input": input_params,
            "result": error_result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)


def preview_generated_code(
    session_id: str,
    file_name: str = "agent.py"
) -> str:
    """
    Preview generated code without writing to disk.
    Uses the same AgentCodeGenerator class for consistency.
    
    Args:
        session_id: Session identifier containing the configuration
        file_name: Name of the file to preview (agent.py, requirements.txt, README.md, etc.)
        
    Returns:
        JSON string with the file content
    """
    try:
        # Get the full configuration
        config_response = get_full_config(session_id)
        config_data = json.loads(config_response)
        
        if not config_data.get("success"):
            return json.dumps({
                "success": False,
                "error": f"Failed to get configuration: {config_data.get('error', 'Unknown error')}"
            }, indent=2)
        
        # Extract the project configuration
        full_config = config_data["config"]
        project_config = full_config["project_config"]
        
        # Create AgentProjectConfig object
        try:
            config_obj = AgentProjectConfig(**project_config)
        except Exception as config_error:
            return json.dumps({
                "success": False,
                "error": f"Configuration parsing error: {str(config_error)}"
            }, indent=2)
        
        # Generate the code using the same AgentCodeGenerator class (without writing to disk)
        generator = AgentCodeGenerator()
        generated_files = generator.generate_from_config(config_obj, output_dir=None)
        
        if file_name not in generated_files:
            available_files = list(generated_files.keys())
            return json.dumps({
                "success": False,
                "error": f"File '{file_name}' not found in generated files",
                "available_files": available_files
            }, indent=2)
        
        return json.dumps({
            "success": True,
            "file_name": file_name,
            "content": generated_files[file_name],
            "available_files": list(generated_files.keys())
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to preview code: {str(e)}"
        }, indent=2)


def validate_configuration(session_id: str) -> str:
    """
    Validate the agent configuration for completeness and correctness.
    
    Args:
        session_id: Session identifier containing the configuration
        
    Returns:
        JSON string with validation results
    """
    input_params = {
        "session_id": session_id
    }
    
    try:
        # Get the full configuration
        config_response = get_full_config(session_id)
        config_data = json.loads(config_response)
        
        if not config_data.get("success"):
            error_result = {
                "success": False,
                "error": f"Failed to get configuration: {config_data.get('error', 'Unknown error')}"
            }
            return json.dumps({
                "tool": "validate_configuration",
                "input": input_params,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            }, indent=2)
        
        # Extract the project configuration
        full_config = config_data["config"]
        project_config = full_config["project_config"]
        
        # Validate the configuration  
        try:
            config_obj = AgentProjectConfig(**project_config)
            validation_errors = validate_agent_config(config_obj)
        except Exception as validation_error:
            error_result = {
                "success": False,
                "valid": False,
                "error": f"Configuration validation error: {str(validation_error)}",
                "message": "Failed to validate configuration due to schema error"
            }
            return json.dumps({
                "tool": "validate_configuration",
                "input": input_params,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            }, indent=2)
        
        if validation_errors:
            error_result = {
                "success": False,
                "valid": False,
                "errors": validation_errors,
                "message": "Configuration validation failed"
            }
            result = error_result
        else:
            result = {
                "success": True,
                "valid": True,
                "message": "Configuration is valid and ready for code generation",
                "summary": {
                    "project_name": project_config["project_name"],
                    "main_agent": project_config["main_agent"],
                    "agent_count": len(project_config["agents"]),
                    "tool_count": len(project_config["tools"]),
                    "requirement_count": len(project_config["requirements"])
                }
            }
        
        return json.dumps({
            "tool": "validate_configuration",
            "input": input_params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Failed to validate configuration: {str(e)}"
        }
        
        return json.dumps({
            "tool": "validate_configuration",
            "input": input_params,
            "result": error_result,
            "timestamp": datetime.now().isoformat()
        }, indent=2) 