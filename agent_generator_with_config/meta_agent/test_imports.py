#!/usr/bin/env python3
"""
Test script to verify all imports work correctly for the meta-agent.
Run this before testing the full system.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test all the import statements."""
    
    print("Testing meta-agent imports...")
    
    try:
        print("1. Testing config...")
        from config import Config
        config = Config()
        print(f"   ✅ Config loaded - Model: {config.agent_settings.model}")
        
        print("2. Testing prompts...")
        from prompts import ORCHESTRATOR_PROMPT
        print(f"   ✅ Prompts loaded - Orchestrator prompt length: {len(ORCHESTRATOR_PROMPT)}")
        
        print("3. Testing config merger tools...")
        from tools.config_merger import create_project, add_agent_to_config
        print("   ✅ Config merger tools loaded")
        
        print("4. Testing code generator tools...")
        from tools.code_generator import generate_agent_code
        print("   ✅ Code generator tools loaded")
        
        print("5. Testing sub-agents...")
        from sub_agents.requirements_analyzer import requirements_analyzer
        from sub_agents.architecture_planner import architecture_planner
        from sub_agents.agent_builder import agent_builder
        from sub_agents.prompt_builder import prompt_builder
        from sub_agents.tool_builder import tool_builder
        print("   ✅ All sub-agents loaded")
        
        print("6. Testing main agent...")
        from agent import root_agent, agent_creator_orchestrator
        print(f"   ✅ Main agent loaded - Name: {root_agent.name}")
        
        print("\n🎉 ALL IMPORTS SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_config_creation():
    """Test creating a simple config."""
    
    print("\nTesting config operations...")
    
    try:
        from tools.config_merger import create_project, get_config_summary
        
        # Test creating a project
        session_id = "test-session-123"
        result = create_project(session_id, "test_project", "A test project")
        print(f"   ✅ Project creation: {result}")
        
        # Test getting summary
        summary = get_config_summary(session_id)
        print(f"   ✅ Config summary: {summary}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Config operation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    
    print("=" * 60)
    print("META-AGENT IMPORT TEST")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic operations
        config_ok = test_config_creation()
        
        if config_ok:
            print("\n🎉 ALL TESTS PASSED! Meta-agent is ready to use.")
            print("\nNext steps:")
            print("1. Run: python main.py simple")
            print("2. Or run: python main.py interactive")
        else:
            print("\n⚠️  Imports OK but config operations failed.")
    else:
        print("\n❌ Import tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main() 