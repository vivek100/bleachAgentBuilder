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
Test configurations for the Agent Generator.
These demonstrate various agent patterns and configurations.
"""

import json
try:
    from .config_schema import AgentProjectConfig, validate_agent_config
    from .code_generator import generate_agent_from_dict
except ImportError:
    from config_schema import AgentProjectConfig, validate_agent_config
    from code_generator import generate_agent_from_dict


# Test Configuration 1: Simple Research Agent
SIMPLE_RESEARCH_AGENT_CONFIG = {
    "project_name": "research_assistant",
    "description": "A research assistant that can search the web and load web pages for analysis",
    "version": "1.0.0",
    "main_agent": "research_coordinator",
    
    "agents": {
        "research_coordinator": {
            "name": "research_coordinator",
            "type": "llm_agent",
            "description": "Main research coordinator that helps users with research tasks",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You are a research assistant that helps users research topics by searching the web and analyzing web pages.

When a user asks for research on a topic:
1. Use google_search to find relevant information
2. Use url_context to load and analyze specific web pages
3. Provide comprehensive, well-sourced answers

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
        "GOOGLE_SEARCH_API_KEY": "your_api_key_here",
        "GOOGLE_SEARCH_ENGINE_ID": "your_engine_id_here"
    }
}


# Test Configuration 2: Customer Service with Memory
CUSTOMER_SERVICE_CONFIG = {
    "project_name": "customer_service_bot",
    "description": "Customer service bot with memory and search capabilities",
    "version": "1.0.0",
    "main_agent": "service_coordinator",
    
    "agents": {
        "service_coordinator": {
            "name": "service_coordinator",
            "type": "llm_agent",
            "description": "Customer service coordinator with memory and search capabilities",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You are a helpful customer service representative. 

You have access to:
- Memory to remember previous conversations and customer details
- Web search to find current information about products/services
- Web page loading to access detailed documentation

Always:
1. Check memory for previous customer interactions
2. Search for current information when needed
3. Provide helpful, accurate, and friendly responses
4. Remember important customer details for future interactions""",
            "tools": ["memory_loader", "memory_preloader", "web_search", "page_loader"],
            "sub_agents": [],
            "config": {
                "temperature": 0.2
            }
        }
    },
    
    "tools": {
        "memory_loader": {
            "name": "memory_loader",
            "type": "builtin",
            "description": "Load relevant memories based on context",
            "builtin_type": "load_memory"
        },
        "memory_preloader": {
            "name": "memory_preloader", 
            "type": "builtin",
            "description": "Preload specific memories at conversation start",
            "builtin_type": "preload_memory"
        },
        "web_search": {
            "name": "web_search",
            "type": "builtin",
            "description": "Search the web for current information",
            "builtin_type": "google_search"
        },
        "page_loader": {
            "name": "page_loader",
            "type": "builtin",
            "description": "Load and analyze web page content",
            "builtin_type": "url_context"
        }
    }
}


# Test Configuration 3: Multi-Agent Sequential Processing
SEQUENTIAL_PROCESSING_CONFIG = {
    "project_name": "document_processor",
    "description": "Sequential document processing system with specialized agents",
    "version": "1.0.0",
    "main_agent": "document_pipeline",
    
    "agents": {
        "content_analyzer": {
            "name": "content_analyzer",
            "type": "llm_agent",
            "description": "Analyzes document content and structure",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You analyze document content and extract key information.

Your job is to:
1. Read and understand the document content
2. Identify key topics, themes, and structure
3. Extract important facts and data points
4. Prepare a structured analysis for the next agent

Return your analysis in a clear, structured format.""",
            "tools": ["page_loader"],
            "sub_agents": [],
            "config": {
                "temperature": 0.1
            }
        },
        
        "fact_checker": {
            "name": "fact_checker",
            "type": "llm_agent",
            "description": "Fact-checks content using web search",
            "model": "gemini-2.0-flash-lite-001", 
            "instruction": """You fact-check information using web search.

Your job is to:
1. Take the analyzed content from the previous agent
2. Identify claims that need verification
3. Search the web for supporting or contradicting evidence
4. Provide a fact-check report with sources

Be thorough and cite all sources.""",
            "tools": ["web_search", "page_loader"],
            "sub_agents": [],
            "config": {
                "temperature": 0.2
            }
        },
        
        "document_pipeline": {
            "name": "document_pipeline",
            "type": "sequential_agent",
            "description": "Sequential document processing pipeline",
            "sub_agents": ["content_analyzer", "fact_checker"]
        }
    },
    
    "tools": {
        "web_search": {
            "name": "web_search",
            "type": "builtin",
            "description": "Search the web for fact-checking",
            "builtin_type": "google_search"
        },
        "page_loader": {
            "name": "page_loader",
            "type": "builtin",
            "description": "Load and analyze web page content",
            "builtin_type": "url_context"
        }
    }
}


# Test Configuration 4: Agent with Custom Function Tool
CUSTOM_TOOL_CONFIG = {
    "project_name": "calculator_agent",
    "description": "Agent with custom mathematical calculation tools",
    "version": "1.0.0",
    "main_agent": "math_assistant",
    
    "agents": {
        "math_assistant": {
            "name": "math_assistant",
            "type": "llm_agent",
            "description": "Mathematical calculation assistant",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": """You are a mathematical assistant that can help with calculations.

When users ask for mathematical operations:
1. Use the available calculation tools for complex math
2. Explain your calculations step by step
3. Show the final result clearly

You have access to basic calculator functions and statistical operations.""",
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
            "description": "Basic mathematical calculations",
            "function_code": """def calculator(expression: str, tool_context: ToolContext) -> float:
    \"\"\"Evaluate a mathematical expression safely.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4")
        tool_context: Tool execution context
        
    Returns:
        Result of the mathematical expression
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
        if isinstance(node, ast.Num):  # number
            return node.n
        elif isinstance(node, ast.BinOp):  # binary operation
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):  # unary operation
            return ops[type(node.op)](eval_expr(node.operand))
        else:
            raise TypeError(f"Unsupported operation: {node}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        result = eval_expr(tree.body)
        
        # Store calculation in context
        if 'calculations' not in tool_context.state:
            tool_context.state['calculations'] = []
        tool_context.state['calculations'].append({
            'expression': expression,
            'result': result
        })
        
        return result
    except Exception as e:
        raise ValueError(f"Invalid mathematical expression: {expression}. Error: {str(e)}")"""
        },
        
        "statistics": {
            "name": "statistics",
            "type": "custom_function",
            "description": "Statistical calculations on number lists",
            "function_code": """def statistics(numbers: list[float], operation: str, tool_context: ToolContext) -> float:
    \"\"\"Perform statistical operations on a list of numbers.
    
    Args:
        numbers: List of numbers to analyze
        operation: Statistical operation (mean, median, mode, std, variance)
        tool_context: Tool execution context
        
    Returns:
        Result of the statistical calculation
    \"\"\"
    import statistics as stats
    
    if not numbers:
        raise ValueError("Cannot perform statistics on empty list")
    
    operations = {
        'mean': stats.mean,
        'median': stats.median,
        'mode': stats.mode,
        'std': stats.stdev,
        'variance': stats.variance,
        'min': min,
        'max': max,
        'sum': sum,
        'count': len
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}. Available: {list(operations.keys())}")
    
    try:
        if operation in ['std', 'variance'] and len(numbers) < 2:
            raise ValueError(f"Need at least 2 numbers for {operation}")
        
        result = operations[operation](numbers)
        
        # Store calculation in context
        if 'statistics' not in tool_context.state:
            tool_context.state['statistics'] = []
        tool_context.state['statistics'].append({
            'numbers': numbers,
            'operation': operation,
            'result': result
        })
        
        return result
    except Exception as e:
        raise ValueError(f"Error calculating {operation}: {str(e)}")"""
        }
    }
}


def test_all_configs():
    """Test all configurations for validity and code generation."""
    configs = [
        ("Simple Research Agent", SIMPLE_RESEARCH_AGENT_CONFIG),
        ("Customer Service Bot", CUSTOMER_SERVICE_CONFIG),
        ("Sequential Processing", SEQUENTIAL_PROCESSING_CONFIG),
        ("Custom Tool Agent", CUSTOM_TOOL_CONFIG),
    ]
    
    for name, config_dict in configs:
        print(f"\n=== Testing {name} ===")
        
        # Validate configuration
        config = AgentProjectConfig(**config_dict)
        errors = validate_agent_config(config)
        
        if errors:
            print(f"❌ Validation errors: {errors}")
            continue
        else:
            print("✅ Configuration valid")
        
        # Generate code
        try:
            files = generate_agent_from_dict(config_dict)
            print(f"✅ Generated {len(files)} files: {list(files.keys())}")
        except Exception as e:
            print(f"❌ Code generation error: {str(e)}")


def save_sample_configs():
    """Save sample configurations as JSON files for reference."""
    configs = {
        "simple_research_agent.json": SIMPLE_RESEARCH_AGENT_CONFIG,
        "customer_service_bot.json": CUSTOMER_SERVICE_CONFIG,
        "sequential_processing.json": SEQUENTIAL_PROCESSING_CONFIG,
        "custom_tool_agent.json": CUSTOM_TOOL_CONFIG,
    }
    
    for filename, config in configs.items():
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Saved: {filename}")


if __name__ == "__main__":
    test_all_configs()
    save_sample_configs() 