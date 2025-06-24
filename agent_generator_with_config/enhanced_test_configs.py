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
Enhanced test configurations demonstrating new features:
1. Custom tool imports and dependencies
2. Environment variables with actual and example values
"""

from config_schema import AgentProjectConfig

# Enhanced configuration with custom imports and dependencies
enhanced_custom_tool_config = {
    "project_name": "enhanced_data_processor",
    "description": "An enhanced agent that processes data with external libraries",
    "version": "1.0.0",
    "main_agent": "data_processor",
    
    "agents": {
        "data_processor": {
            "name": "data_processor",
            "type": "llm_agent",
            "description": "Processes data using pandas and requests",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": "You are a data processing assistant. Use the available tools to fetch and analyze data.",
            "tools": ["fetch_data", "analyze_data", "export_results"]
        }
    },
    
    "tools": {
        "fetch_data": {
            "name": "fetch_data",
            "type": "custom_function",
            "description": "Fetch data from a URL using requests",
            "imports": [
                "import requests",
                "import json"
            ],
            "dependencies": [
                "requests>=2.31.0"
            ],
            "function_code": """def fetch_data(url: str) -> str:
    \"\"\"Fetch data from a URL.\"\"\"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error fetching data: {str(e)}\""""
        },
        
        "analyze_data": {
            "name": "analyze_data", 
            "type": "custom_function",
            "description": "Analyze data using pandas",
            "imports": [
                "import pandas as pd",
                "import json"
            ],
            "dependencies": [
                "pandas>=2.0.0"
            ],
            "function_code": """def analyze_data(data_json: str) -> str:
    \"\"\"Analyze JSON data using pandas.\"\"\"
    try:
        data = json.loads(data_json)
        df = pd.DataFrame(data)
        
        analysis = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "summary": df.describe().to_dict() if df.select_dtypes(include='number').shape[1] > 0 else "No numeric columns"
        }
        
        return json.dumps(analysis, indent=2, default=str)
    except Exception as e:
        return f"Error analyzing data: {str(e)}\""""
        },
        
        "export_results": {
            "name": "export_results",
            "type": "custom_function", 
            "description": "Export results to CSV using pandas",
            "imports": [
                "import pandas as pd",
                "import json",
                "from datetime import datetime",
                "from typing import Optional"
            ],
            "dependencies": [
                "pandas>=2.0.0"
            ],
            "function_code": """def export_results(data_json: str, filename: Optional[str] = None) -> str:
    \"\"\"Export data to CSV file.\"\"\"
    try:
        data = json.loads(data_json)
        df = pd.DataFrame(data)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        return f"Data exported to {filename} successfully. Shape: {df.shape}"
    except Exception as e:
        return f"Error exporting data: {str(e)}\""""
        }
    },
    
    "requirements": [
        "python-dotenv>=1.0.0"
    ],
    
    "environment_variables": {
        "API_KEY": "sk-1234567890abcdef",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb",
        "DEBUG": "true"
    },
    
    "environment_variables_example": {
        "API_KEY": "your-api-key-here",
        "DATABASE_URL": "postgresql://username:password@host:port/database",
        "DEBUG": "false"
    }
}

# Configuration with web scraping capabilities
web_scraper_config = {
    "project_name": "web_scraper_agent",
    "description": "An agent that scrapes and processes web content",
    "version": "1.0.0", 
    "main_agent": "scraper",
    
    "agents": {
        "scraper": {
            "name": "scraper",
            "type": "llm_agent",
            "description": "Web scraping and content analysis agent",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": "You are a web scraping assistant. Use the tools to fetch and analyze web content.",
            "tools": ["scrape_page", "extract_links", "save_content"]
        }
    },
    
    "tools": {
        "scrape_page": {
            "name": "scrape_page",
            "type": "custom_function",
            "description": "Scrape content from a web page",
            "imports": [
                "import requests",
                "from bs4 import BeautifulSoup",
                "import re"
            ],
            "dependencies": [
                "requests>=2.31.0",
                "beautifulsoup4>=4.12.0",
                "lxml>=4.9.0"
            ],
            "function_code": """def scrape_page(url: str, selector: Optional[str] = None) -> str:
    \"\"\"Scrape content from a web page.\"\"\"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if selector:
            elements = soup.select(selector)
            content = '\\n'.join([elem.get_text().strip() for elem in elements])
        else:
            content = soup.get_text()
        
        # Clean up whitespace
        content = re.sub(r'\\s+', ' ', content).strip()
        
        return content[:5000]  # Limit to 5000 chars
    except Exception as e:
        return f"Error scraping page: {str(e)}\""""
        },
        
        "extract_links": {
            "name": "extract_links",
            "type": "custom_function",
            "description": "Extract all links from a web page",
            "imports": [
                "import requests", 
                "from bs4 import BeautifulSoup",
                "from urllib.parse import urljoin, urlparse"
            ],
            "dependencies": [
                "requests>=2.31.0",
                "beautifulsoup4>=4.12.0"
            ],
            "function_code": """def extract_links(url: str, internal_only: bool = False) -> str:
    \"\"\"Extract all links from a web page.\"\"\"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        base_domain = urlparse(url).netloc
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            
            if internal_only and urlparse(full_url).netloc != base_domain:
                continue
                
            links.append({
                'text': link.get_text().strip()[:100],
                'url': full_url
            })
        
        return str(links[:50])  # Limit to 50 links
    except Exception as e:
        return f"Error extracting links: {str(e)}\""""
        },
        
        "save_content": {
            "name": "save_content",
            "type": "custom_function",
            "description": "Save content to a file",
            "imports": [
                "import os",
                "from datetime import datetime",
                "from typing import Optional"
            ],
            "function_code": """def save_content(content: str, filename: Optional[str] = None) -> str:
    \"\"\"Save content to a file.\"\"\"
    try:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_content_{timestamp}.txt"
        
        # Create directory if it doesn't exist
        os.makedirs('scraped_data', exist_ok=True)
        filepath = os.path.join('scraped_data', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Content saved to {filepath}. Size: {len(content)} characters"
    except Exception as e:
        return f"Error saving content: {str(e)}\""""
        }
    },
    
    "environment_variables": {
        "SCRAPER_USER_AGENT": "MyBot/1.0",
        "MAX_REQUESTS_PER_MINUTE": "60",
        "OUTPUT_DIR": "./scraped_data"
    },
    
    "environment_variables_example": {
        "SCRAPER_USER_AGENT": "YourBot/1.0 (contact@example.com)",
        "MAX_REQUESTS_PER_MINUTE": "30",
        "OUTPUT_DIR": "./output"
    }
}

# Multi-agent workflow with environment variables
workflow_config = {
    "project_name": "data_workflow",
    "description": "Multi-agent workflow for data processing",
    "version": "1.0.0",
    "main_agent": "coordinator",
    
    "agents": {
        "coordinator": {
            "name": "coordinator",
            "type": "sequential_agent",
            "description": "Coordinates the data processing workflow",
            "sub_agents": ["fetcher", "processor", "reporter"]
        },
        
        "fetcher": {
            "name": "fetcher",
            "type": "llm_agent",
            "description": "Fetches data from external sources",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": "You fetch data from APIs and databases. Use the fetch_api_data tool.",
            "tools": ["fetch_api_data"]
        },
        
        "processor": {
            "name": "processor", 
            "type": "llm_agent",
            "description": "Processes and transforms data",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": "You process and clean data. Use the process_data tool.",
            "tools": ["process_data"]
        },
        
        "reporter": {
            "name": "reporter",
            "type": "llm_agent", 
            "description": "Generates reports from processed data",
            "model": "gemini-2.0-flash-lite-001",
            "instruction": "You generate reports and visualizations. Use the generate_report tool.",
            "tools": ["generate_report"]
        }
    },
    
    "tools": {
        "fetch_api_data": {
            "name": "fetch_api_data",
            "type": "custom_function",
            "description": "Fetch data from API with authentication",
            "imports": [
                "import requests",
                "import os"
            ],
            "dependencies": [
                "requests>=2.31.0"
            ],
            "function_code": """def fetch_api_data(endpoint: str) -> str:
    \"\"\"Fetch data from API using environment variables for auth.\"\"\"
    try:
        api_key = os.getenv('API_KEY')
        base_url = os.getenv('API_BASE_URL', 'https://api.example.com')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        url = f"{base_url}/{endpoint}"
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.text
    except Exception as e:
        return f"Error fetching API data: {str(e)}\""""
        },
        
        "process_data": {
            "name": "process_data",
            "type": "custom_function",
            "description": "Process data with configurable parameters",
            "imports": [
                "import json",
                "import os"
            ],
            "function_code": """def process_data(raw_data: str) -> str:
    \"\"\"Process raw data using environment configuration.\"\"\"
    try:
        data = json.loads(raw_data)
        
        # Get processing parameters from environment
        max_records = int(os.getenv('MAX_RECORDS', '1000'))
        filter_field = os.getenv('FILTER_FIELD', 'status')
        filter_value = os.getenv('FILTER_VALUE', 'active')
        
        # Process data
        if isinstance(data, list):
            processed = [
                item for item in data[:max_records] 
                if item.get(filter_field) == filter_value
            ]
        else:
            processed = data
        
        return json.dumps(processed, indent=2)
    except Exception as e:
        return f"Error processing data: {str(e)}\""""
        },
        
        "generate_report": {
            "name": "generate_report",
            "type": "custom_function",
            "description": "Generate report with environment-based configuration",
            "imports": [
                "import json",
                "import os",
                "from datetime import datetime",
                "from typing import Optional"
            ],
            "function_code": """def generate_report(processed_data: str) -> str:
    \"\"\"Generate report using environment settings.\"\"\"
    try:
        data = json.loads(processed_data)
        
        # Get report settings from environment
        report_format = os.getenv('REPORT_FORMAT', 'summary')
        output_dir = os.getenv('OUTPUT_DIR', './reports')
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if report_format == 'detailed':
            report = {
                'timestamp': timestamp,
                'total_records': len(data) if isinstance(data, list) else 1,
                'data': data
            }
        else:
            report = {
                'timestamp': timestamp,
                'summary': f"Processed {len(data) if isinstance(data, list) else 1} records"
            }
        
        # Save report
        os.makedirs(output_dir, exist_ok=True)
        filename = f"report_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return f"Report generated: {filepath}"
    except Exception as e:
        return f"Error generating report: {str(e)}\""""
        }
    },
    
    "environment_variables": {
        "API_KEY": "prod-key-12345",
        "API_BASE_URL": "https://api.production.com",
        "MAX_RECORDS": "5000", 
        "FILTER_FIELD": "status",
        "FILTER_VALUE": "published",
        "REPORT_FORMAT": "detailed",
        "OUTPUT_DIR": "./production_reports"
    },
    
    "environment_variables_example": {
        "API_KEY": "your-api-key-here",
        "API_BASE_URL": "https://api.example.com",
        "MAX_RECORDS": "1000",
        "FILTER_FIELD": "status", 
        "FILTER_VALUE": "active",
        "REPORT_FORMAT": "summary",
        "OUTPUT_DIR": "./reports"
    }
} 