#!/usr/bin/env python3
# Quick start script for my_test_agent

from agent import root_agent

def main():
    print("Starting my_test_agent...")
    print("Main agent: main_agent")
    print("Available agents: ['main_agent']")
    print("Available tools: []")
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
