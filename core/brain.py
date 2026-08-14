import json
import config
from openai import OpenAI

# 1. Import your custom tools
from tools.system_tools import open_windows_app, adjust_volume, check_system_status
from tools.web_tools import search_web, open_website

# Initialize the client pointing to NVIDIA's API endpoint
client = OpenAI(
    base_url=config.NVIDIA_API_BASE_URL,
    api_key=config.NVIDIA_API_KEY
)

# 2. Map string names to the imported Python functions
available_tools = {
    "open_windows_app": open_windows_app,
    "adjust_volume": adjust_volume,
    "check_system_status": check_system_status,
    "search_web": search_web,
    "open_website": open_website
}

# 3. Define the comprehensive Tool Schema for Nemotron
tools = [
    {
        "type": "function",
        "function": {
            "name": "open_windows_app",
            "description": "Launches a desktop application on the Windows host machine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "The executable name or common name of the app."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_volume",
            "description": "Adjusts the Windows system volume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["up", "down", "mute"], "description": "The direction to adjust volume."}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_system_status",
            "description": "Retrieves the current CPU load and available RAM of the host machine.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Opens the Windows web browser and performs a Google search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search term or question."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Opens a specific URL in the Windows web browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The full URL of the website."}
                },
                "required": ["url"]
            }
        }
    }
]

# 4. Process Prompt through Nemotron
def run_agent_step(user_prompt: str):
    messages = [
        {"role": "system", "content": "You are DEMON Cell, an AI system controller. Execute user actions efficiently using your available tools."},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=config.NEMOTRON_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Check if Nemotron decided to call a tool
        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                if func_name in available_tools:
                    print(f"[Agent Tool Execution]: Calling {func_name} with {args}")
                    result = available_tools[func_name](**args)
                    print(f"[Result]: {result}")
                    return result
        
        return message.content

    except Exception as e:
        print(f"[Nemotron Brain Error]: {str(e)}")
        return "I am having trouble connecting to my neural processing center."

if __name__ == "__main__":
    # Test Run
    run_agent_step("Please check the system status.")