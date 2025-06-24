#!/usr/bin/env python3
# Quick start script for weather_forecast_agent

from agent import root_agent

def main():
    print("Starting weather_forecast_agent...")
    print("Main agent: forecaster")
    print("Available agents: ['location_identifier', 'weather_fetcher', 'weather_agent', 'weather_data_retriever', 'forecaster']")
    print("Available tools: ['web_search', 'weather_api']")
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
