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
Main test runner for the Agent Generator with Config.
This demonstrates and tests the config-to-code generation functionality.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the parent directory to the Python path to enable imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from .config_schema import AgentProjectConfig, validate_agent_config, get_default_model
    from .code_generator import AgentCodeGenerator, generate_agent_from_dict
    from .test_configs import (
        SIMPLE_RESEARCH_AGENT_CONFIG,
        CUSTOMER_SERVICE_CONFIG,
        SEQUENTIAL_PROCESSING_CONFIG,
        CUSTOM_TOOL_CONFIG
    )
except ImportError:
    from config_schema import AgentProjectConfig, validate_agent_config, get_default_model
    from code_generator import AgentCodeGenerator, generate_agent_from_dict
    from test_configs import (
        SIMPLE_RESEARCH_AGENT_CONFIG,
        CUSTOMER_SERVICE_CONFIG,
        SEQUENTIAL_PROCESSING_CONFIG,
        CUSTOM_TOOL_CONFIG
    )


def test_config_validation():
    """Test configuration validation."""
    print("=== Testing Configuration Validation ===")
    
    configs = [
        ("Simple Research Agent", SIMPLE_RESEARCH_AGENT_CONFIG),
        ("Customer Service Bot", CUSTOMER_SERVICE_CONFIG),
        ("Sequential Processing", SEQUENTIAL_PROCESSING_CONFIG),
        ("Custom Tool Agent", CUSTOM_TOOL_CONFIG),
    ]
    
    for name, config_dict in configs:
        print(f"\nTesting {name}...")
        
        try:
            # Create Pydantic model
            config = AgentProjectConfig(**config_dict)
            print(f"  ✅ Pydantic validation passed")
            
            # Run custom validation
            errors = validate_agent_config(config)
            if errors:
                print(f"  ❌ Custom validation errors: {errors}")
            else:
                print(f"  ✅ Custom validation passed")
                
        except Exception as e:
            print(f"  ❌ Pydantic validation failed: {str(e)}")


def test_code_generation():
    """Test code generation functionality."""
    print("\n=== Testing Code Generation ===")
    
    configs = [
        ("Simple Research Agent", SIMPLE_RESEARCH_AGENT_CONFIG),
        ("Customer Service Bot", CUSTOMER_SERVICE_CONFIG),
        ("Sequential Processing", SEQUENTIAL_PROCESSING_CONFIG),
        ("Custom Tool Agent", CUSTOM_TOOL_CONFIG),
    ]
    
    for name, config_dict in configs:
        print(f"\nGenerating code for {name}...")
        
        try:
            # Generate code
            files = generate_agent_from_dict(config_dict)
            
            print(f"  ✅ Generated {len(files)} files:")
            for filename in files.keys():
                print(f"    - {filename}")
                
            # Check that main files exist
            required_files = ["agent.py", "__init__.py", "requirements.txt", "README.md"]
            for required_file in required_files:
                if required_file in files:
                    print(f"    ✅ {required_file} generated")
                else:
                    print(f"    ❌ {required_file} missing")
                    
        except Exception as e:
            print(f"  ❌ Code generation failed: {str(e)}")


def test_generated_agent_syntax():
    """Test that generated agent code has valid Python syntax."""
    print("\n=== Testing Generated Code Syntax ===")
    
    configs = [
        ("Simple Research Agent", SIMPLE_RESEARCH_AGENT_CONFIG),
        ("Customer Service Bot", CUSTOMER_SERVICE_CONFIG),
        ("Sequential Processing", SEQUENTIAL_PROCESSING_CONFIG),
        ("Custom Tool Agent", CUSTOM_TOOL_CONFIG),
    ]
    
    for name, config_dict in configs:
        print(f"\nTesting syntax for {name}...")
        
        try:
            # Generate code
            files = generate_agent_from_dict(config_dict)
            
            # Check Python syntax for agent.py
            if "agent.py" in files:
                agent_code = files["agent.py"]
                
                # Try to compile the code to check syntax
                compile(agent_code, f"{name}_agent.py", "exec")
                print(f"  ✅ agent.py syntax is valid")
            else:
                print(f"  ❌ agent.py not generated")
                
        except SyntaxError as e:
            print(f"  ❌ Syntax error in agent.py: {str(e)}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def test_full_agent_generation():
    """Test full agent generation to disk."""
    print("\n=== Testing Full Agent Generation to Disk ===")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Test with Simple Research Agent
        config_dict = SIMPLE_RESEARCH_AGENT_CONFIG
        agent_dir = os.path.join(temp_dir, "research_agent")
        
        try:
            # Generate agent to disk
            files = generate_agent_from_dict(config_dict, agent_dir)
            
            print(f"✅ Generated agent to: {agent_dir}")
            print(f"✅ Files created: {list(files.keys())}")
            
            # Verify files exist on disk
            agent_path = Path(agent_dir)
            for filename in files.keys():
                file_path = agent_path / filename
                if file_path.exists():
                    print(f"  ✅ {filename} exists on disk ({file_path.stat().st_size} bytes)")
                else:
                    print(f"  ❌ {filename} missing from disk")
                    
            # Try to import the generated agent (syntax check)
            sys.path.insert(0, agent_dir)
            try:
                import agent
                print(f"  ✅ Agent module imports successfully")
                if hasattr(agent, 'root_agent'):
                    print(f"  ✅ root_agent is defined")
                else:
                    print(f"  ❌ root_agent not found in module")
            except ImportError as e:
                print(f"  ❌ Failed to import agent: {str(e)}")
            finally:
                # Clean up sys.path
                if agent_dir in sys.path:
                    sys.path.remove(agent_dir)
                    
        except Exception as e:
            print(f"❌ Full generation failed: {str(e)}")


def test_model_from_environment():
    """Test that model configuration uses environment variables correctly."""
    print("\n=== Testing Model Configuration from Environment ===")
    
    # Test default model
    default_model = get_default_model()
    print(f"Default model: {default_model}")
    
    # Test with environment variable set
    os.environ["DEFAULT_MODEL"] = "test-model-123"
    env_model = get_default_model()
    print(f"Model from environment: {env_model}")
    
    # Clean up environment
    if "DEFAULT_MODEL" in os.environ:
        del os.environ["DEFAULT_MODEL"]
    
    if env_model == "test-model-123":
        print("✅ Environment variable model configuration works")
    else:
        print("❌ Environment variable model configuration failed")


def print_sample_generated_code():
    """Print sample generated code for review."""
    print("\n=== Sample Generated Code ===")
    
    # Generate code for simple research agent
    files = generate_agent_from_dict(SIMPLE_RESEARCH_AGENT_CONFIG)
    
    print(f"\nGenerated agent.py for Simple Research Agent:")
    print("=" * 60)
    print(files["agent.py"])
    print("=" * 60)


def main():
    """Run all tests."""
    print("🚀 ADK Agent Generator with Config - Test Suite")
    print("=" * 60)
    
    # Run all tests
    test_config_validation()
    test_code_generation()
    test_generated_agent_syntax()
    test_full_agent_generation()
    test_model_from_environment()
    
    # Print sample for manual review
    print_sample_generated_code()
    
    print("\n🎉 All tests completed!")
    print("\nNext steps:")
    print("1. Review the generated code above")
    print("2. Test running a generated agent with: adk cli <generated_agent_dir>/agent.py")
    print("3. Create your own configurations using the schema")


if __name__ == "__main__":
    main() 