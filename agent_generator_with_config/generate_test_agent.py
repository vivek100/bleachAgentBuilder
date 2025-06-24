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
Generate a test agent for validation.
This creates a real agent that can be tested with the ADK CLI.
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config_schema import AgentProjectConfig, validate_agent_config
    from code_generator import generate_agent_from_dict
except ImportError:
    print("Error: Could not import modules. Make sure you're in the correct directory.")
    sys.exit(1)


# Simple Test Agent Configuration (no external dependencies)
TEST_AGENT_CONFIG = {
    "project_name": "simple_test_agent",
    "description": "A simple test agent with basic functionality for validation",
    "version": "1.0.0",
    "main_agent": "test_coordinator",
    
    "agents": {
        "test_coordinator": {
            "name": "test_coordinator",
            "type": "llm_agent",
            "description": "Main test coordinator that demonstrates basic ADK functionality",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You are a helpful test assistant.

Your capabilities:
1. Answer general questions
2. Provide helpful information
3. Assist with basic tasks

You are a basic conversational agent for testing purposes. Always be helpful and provide clear, accurate responses.""",
            "tools": [],
            "sub_agents": [],
            "config": {
                "temperature": 0.7
            }
        }
    },
    
    "tools": {},
    
    "requirements": [],
    "environment_variables": {}
}


# Custom Function Tool Example
CUSTOM_TOOL_TEST_CONFIG = {
    "project_name": "custom_tool_test_agent",
    "description": "Test agent with custom function tools",
    "version": "1.0.0",
    "main_agent": "calculator_agent",
    
    "agents": {
        "calculator_agent": {
            "name": "calculator_agent",
            "type": "llm_agent",
            "description": "Agent that can perform mathematical calculations",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You are a mathematical assistant.

When users ask for calculations:
1. Use the calculator tool for mathematical expressions
2. Use the statistics tool for statistical operations
3. Explain your calculations clearly

You have access to safe mathematical evaluation and basic statistics.""",
            "tools": ["calculator", "statistics"],
            "sub_agents": [],
            "config": {
                "temperature": 0.1
            }
        }
    },
    
    "tools": {
        "calculator": {
            "name": "calculator",
            "type": "custom_function",
            "description": "Safe mathematical expression evaluator",
            "function_code": """def calculator(expression: str, tool_context: ToolContext) -> float:
    \"\"\"Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression (e.g., "2 + 3 * 4")
        tool_context: Tool execution context
        
    Returns:
        Result of the calculation
    \"\"\"
    import ast
    import operator
    
    # Supported operations
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](eval_expr(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {type(node).__name__}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
        
        # Store in context
        if 'calculations' not in tool_context.state:
            tool_context.state['calculations'] = []
        tool_context.state['calculations'].append({
            'expression': expression,
            'result': result
        })
        
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression '{expression}': {str(e)}")"""
        },
        
        "statistics": {
            "name": "statistics",
            "type": "custom_function",
            "description": "Basic statistical operations",
            "function_code": """def statistics(numbers: List[float], operation: str, tool_context: ToolContext) -> float:
    \"\"\"Perform statistical operations on a list of numbers.
    
    Args:
        numbers: List of numbers
        operation: Operation (mean, median, sum, min, max, count)
        tool_context: Tool execution context
        
    Returns:
        Statistical result
    \"\"\"
    if not numbers:
        raise ValueError("Cannot perform statistics on empty list")
    
    # Convert to floats
    try:
        nums = [float(x) for x in numbers]
    except (ValueError, TypeError):
        raise ValueError("All values must be numeric")
    
    operations = {
        'mean': lambda x: sum(x) / len(x),
        'median': lambda x: sorted(x)[len(x)//2] if len(x) % 2 == 1 else (sorted(x)[len(x)//2-1] + sorted(x)[len(x)//2]) / 2,
        'sum': sum,
        'min': min,
        'max': max,
        'count': len
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}. Available: {list(operations.keys())}")
    
    result = operations[operation](nums)
    
    # Store in context
    if 'statistics' not in tool_context.state:
        tool_context.state['statistics'] = []
    tool_context.state['statistics'].append({
        'numbers': numbers,
        'operation': operation,
        'result': result
    })
    
    return float(result)"""
        }
    }
}


# Web Search Agent (requires API keys)
WEB_SEARCH_AGENT_CONFIG = {
    "project_name": "web_search_agent",
    "description": "Agent with web search capabilities (requires API configuration)",
    "version": "1.0.0",
    "main_agent": "search_coordinator",
    
    "agents": {
        "search_coordinator": {
            "name": "search_coordinator",
            "type": "llm_agent",
            "description": "Agent that can search the web and analyze pages",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You are a research assistant with web search capabilities.

Your capabilities:
1. Search the web for current information
2. Load and analyze web page content
3. Provide well-researched answers with sources

When users ask for information:
1. Use google_search to find relevant results
2. Use url_context to analyze specific pages
3. Provide comprehensive answers with citations

Always cite your sources and provide links when possible.""",
            "tools": ["web_search", "page_loader"],
            "sub_agents": [],
            "config": {
                "temperature": 0.3
            }
        }
    },
    
    "tools": {
        "web_search": {
            "name": "web_search",
            "type": "builtin",
            "description": "Search the web using Google Search",
            "builtin_type": "google_search"
        },
        "page_loader": {
            "name": "page_loader",
            "type": "builtin",
            "description": "Load and analyze web page content",
            "builtin_type": "url_context"
        }
    },
    
    "requirements": [],
    "environment_variables": {
        "GOOGLE_SEARCH_API_KEY": "your_google_search_api_key_here",
        "GOOGLE_SEARCH_ENGINE_ID": "your_search_engine_id_here"
    }
}


def generate_test_agents():
    """Generate test agents to validate functionality."""
    
    # Create test directories
    base_dir = Path(__file__).parent
    test_dir = base_dir / "generated_test_agents"
    test_dir.mkdir(exist_ok=True)
    
    agents = [
        ("simple_test_agent", TEST_AGENT_CONFIG),
        ("custom_tool_test_agent", CUSTOM_TOOL_TEST_CONFIG),
        ("web_search_agent", WEB_SEARCH_AGENT_CONFIG),
    ]
    
    for agent_name, config_dict in agents:
        print(f"\n=== Generating {agent_name} ===")
        
        # Validate configuration
        try:
            config = AgentProjectConfig(**config_dict)
            errors = validate_agent_config(config)
            
            if errors:
                print(f"❌ Validation errors: {errors}")
                continue
            else:
                print("✅ Configuration validated")
        except Exception as e:
            print(f"❌ Configuration error: {str(e)}")
            continue
        
        # Generate agent
        try:
            agent_dir = test_dir / agent_name
            files = generate_agent_from_dict(config_dict, str(agent_dir))
            
            print(f"✅ Generated {len(files)} files to: {agent_dir}")
            for filename in files.keys():
                print(f"  - {filename}")
                
            # Print usage instructions
            print(f"\n📋 To test this agent:")
            print(f"   cd {agent_dir}")
            if agent_name == "simple_test_agent":
                print(f"   adk cli agent.py  # No setup required!")
            elif agent_name == "custom_tool_test_agent":
                print(f"   adk cli agent.py  # Custom tools work out of the box!")
            else:
                print(f"   # Set up environment variables first")
                print(f"   adk cli agent.py")
            
        except Exception as e:
            print(f"❌ Generation failed: {str(e)}")
    
    print(f"\n🎉 Test agents generated in: {test_dir}")
    print(f"\n💡 Next steps:")
    print(f"1. Navigate to a generated agent directory")
    print(f"2. For simple_test_agent: Run immediately with 'adk cli agent.py'")
    print(f"3. For web_search_agent: Set up API keys in environment first")
    print(f"4. Test the agent functionality")


if __name__ == "__main__":
    generate_test_agents() 