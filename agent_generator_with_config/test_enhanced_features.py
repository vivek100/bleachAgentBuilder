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
Test script for enhanced agent generator features:
1. Custom tool imports and dependencies
2. Environment variables (actual and example values)
"""

import json
import os
import shutil
from pathlib import Path

from config_schema import AgentProjectConfig, validate_agent_config
from code_generator import AgentCodeGenerator
from enhanced_test_configs import (
    enhanced_custom_tool_config,
    web_scraper_config,
    workflow_config
)


def test_enhanced_config_validation():
    """Test that enhanced configurations are valid."""
    print("Testing enhanced configuration validation...")
    
    configs = [
        ("enhanced_custom_tool_config", enhanced_custom_tool_config),
        ("web_scraper_config", web_scraper_config),
        ("workflow_config", workflow_config)
    ]
    
    for name, config_dict in configs:
        print(f"\n--- Testing {name} ---")
        
        # Validate with Pydantic
        try:
            config = AgentProjectConfig(**config_dict)
            print(f"✓ Pydantic validation passed")
        except Exception as e:
            print(f"✗ Pydantic validation failed: {e}")
            continue
        
        # Validate with custom rules
        errors = validate_agent_config(config)
        if errors:
            print(f"✗ Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"✓ Configuration validation passed")


def test_code_generation():
    """Test code generation with enhanced features."""
    print("\n" + "="*60)
    print("Testing code generation with enhanced features...")
    
    generator = AgentCodeGenerator()
    
    configs = [
        ("enhanced_data_processor", enhanced_custom_tool_config),
        ("web_scraper_agent", web_scraper_config),
        ("data_workflow", workflow_config)
    ]
    
    for name, config_dict in configs:
        print(f"\n--- Generating {name} ---")
        
        try:
            config = AgentProjectConfig(**config_dict)
            output_dir = f"./generated_test_agents/{name}"
            
            # Clean up previous generation
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            
            # Generate files
            files = generator.generate_from_config(config, output_dir)
            
            print(f"✓ Generated {len(files)} files:")
            for filename in files.keys():
                file_path = Path(output_dir) / filename
                if file_path.exists():
                    print(f"  ✓ {filename} ({file_path.stat().st_size} bytes)")
                else:
                    print(f"  ✗ {filename} (not found)")
            
            # Test specific enhanced features
            test_enhanced_features(output_dir, config)
            
        except Exception as e:
            print(f"✗ Generation failed: {e}")
            import traceback
            traceback.print_exc()


def test_enhanced_features(output_dir: str, config: AgentProjectConfig):
    """Test specific enhanced features in generated files."""
    
    # Test imports in agent.py
    agent_file = Path(output_dir) / "agent.py"
    if agent_file.exists():
        content = agent_file.read_text()
        
        # Check for custom imports
        custom_imports = set()
        for tool in config.tools.values():
            if tool.type == "custom_function" and tool.imports:
                custom_imports.update(tool.imports)
        
        for import_stmt in custom_imports:
            if import_stmt.strip() in content:
                print(f"  ✓ Custom import found: {import_stmt.strip()}")
            else:
                print(f"  ✗ Custom import missing: {import_stmt.strip()}")
    
    # Test requirements.txt
    req_file = Path(output_dir) / "requirements.txt"
    if req_file.exists():
        content = req_file.read_text()
        
        # Check for custom dependencies
        custom_deps = set()
        for tool in config.tools.values():
            if tool.type == "custom_function" and tool.dependencies:
                custom_deps.update(tool.dependencies)
        
        for dep in custom_deps:
            if dep.strip() in content:
                print(f"  ✓ Custom dependency found: {dep.strip()}")
            else:
                print(f"  ✗ Custom dependency missing: {dep.strip()}")
    
    # Test .env files
    env_file = Path(output_dir) / ".env"
    env_example_file = Path(output_dir) / ".env.example"
    
    if config.environment_variables:
        if env_file.exists():
            content = env_file.read_text()
            for key, value in config.environment_variables.items():
                if f"{key}={value}" in content:
                    print(f"  ✓ Environment variable found in .env: {key}")
                else:
                    print(f"  ✗ Environment variable missing in .env: {key}")
        else:
            print(f"  ✗ .env file not generated")
    
    if config.environment_variables_example or config.environment_variables:
        if env_example_file.exists():
            content = env_example_file.read_text()
            env_vars = config.environment_variables_example or config.environment_variables
            for key in env_vars.keys():
                if f"{key}=" in content:
                    print(f"  ✓ Environment variable found in .env.example: {key}")
                else:
                    print(f"  ✗ Environment variable missing in .env.example: {key}")
        else:
            print(f"  ✗ .env.example file not generated")


def test_import_generated_agents():
    """Test that generated agents can be imported successfully."""
    print("\n" + "="*60)
    print("Testing import of generated agents...")
    
    import sys
    
    configs = [
        ("enhanced_data_processor", enhanced_custom_tool_config),
        ("web_scraper_agent", web_scraper_config),
        ("data_workflow", workflow_config)
    ]
    
    for name, config_dict in configs:
        print(f"\n--- Testing import of {name} ---")
        
        output_dir = f"./generated_test_agents/{name}"
        agent_file = Path(output_dir) / "agent.py"
        
        if not agent_file.exists():
            print(f"✗ Agent file not found: {agent_file}")
            continue
        
        try:
            # Add the output directory to Python path
            if str(output_dir) not in sys.path:
                sys.path.insert(0, str(output_dir))
            
            # Try to import the agent module
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent", agent_file)
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)
            
            # Check if root_agent exists
            if hasattr(agent_module, 'root_agent'):
                print(f"✓ Successfully imported agent with root_agent")
                print(f"  Root agent type: {type(agent_module.root_agent).__name__}")
            else:
                print(f"✗ Agent module missing 'root_agent' attribute")
            
        except Exception as e:
            print(f"✗ Import failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Clean up sys.path
            if str(output_dir) in sys.path:
                sys.path.remove(str(output_dir))


def print_feature_summary():
    """Print a summary of enhanced features."""
    print("\n" + "="*60)
    print("ENHANCED FEATURES SUMMARY")
    print("="*60)
    
    print("\n1. CUSTOM TOOL IMPORTS:")
    print("   - Tools can specify additional imports needed")
    print("   - Imports are automatically added to generated agent.py")
    print("   - Example: ['import requests', 'from bs4 import BeautifulSoup']")
    
    print("\n2. CUSTOM TOOL DEPENDENCIES:")
    print("   - Tools can specify Python packages required")
    print("   - Dependencies are automatically added to requirements.txt")
    print("   - Example: ['requests>=2.31.0', 'beautifulsoup4>=4.12.0']")
    
    print("\n3. ENVIRONMENT VARIABLES:")
    print("   - Support for actual values (written to .env)")
    print("   - Support for example values (written to .env.example)")
    print("   - Automatic generation of both files")
    print("   - Tools can use os.getenv() to access environment variables")
    
    print("\n4. GENERATED FILES:")
    print("   - agent.py (with custom imports)")
    print("   - requirements.txt (with custom dependencies)")
    print("   - .env (with actual environment values)")
    print("   - .env.example (with example/placeholder values)")
    print("   - README.md (updated documentation)")
    print("   - __init__.py (package initialization)")


if __name__ == "__main__":
    print("ADK Agent Generator - Enhanced Features Test")
    print("="*60)
    
    # Run all tests
    test_enhanced_config_validation()
    test_code_generation()
    test_import_generated_agents()
    print_feature_summary()
    
    print(f"\n✓ Enhanced features testing completed!")
    print(f"Generated agents are available in: ./generated_test_agents/") 