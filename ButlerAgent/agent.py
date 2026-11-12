import dotenv
import os
from openai import OpenAI
from typing import Union
import json
from openai.types.responses import FunctionToolParam

dotenv.load_dotenv()

TOOLS_REGISTRY: list[FunctionToolParam] = [
    {
        "type": "function",
        "name": "check_weather",
        "strict": True,
        "description": "Check weather conditions. Use when user asks about weather or what clothes to wear.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        }
    },
    {
        "type": "function",
        "name": "get_wardrobe_items",
        "strict": True,
        "description": "Lists all clothing items in the wardrobe with their status (clean/dirty).",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        }
    },
    {
        "type": "function",
        "name": "wash_clothing",
        "strict": True,
        "description": "Washes a dirty clothing item, changing its status to clean.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_name": {
                    "type": "string",
                    "description": "Name of the cloth"
                }
            },
            "required": ["item_name"],
            "additionalProperties": False,
        }
    }
]


def check_weather() -> str:
    return "Cold, rainy"


WARDROBE = {
    "blue sweater": "dirty",
    "brown jacket": "dirty"
}


def get_wardrobe_items() -> str:
    return "\n".join(f"{item}: {stats}" for item, stats in WARDROBE.items())


def wash_clothing(item_name) -> str:
    if item_name in WARDROBE:
        WARDROBE[item_name] = "clean"
        return f"{item_name} is now clean"
    return f"ERROR: {item_name} not found"


TOOL_NAME_TO_FUNC = {
    "check_weather": check_weather,
    "get_wardrobe_items": get_wardrobe_items,
    "wash_clothing": wash_clothing
}

client = OpenAI(api_key=os.getenv("LITELLM_API_KEY"), base_url=os.getenv("LITELLM_BASE_URL"))

SYSTEM_PROMPT = """
When the user asks what to wear:
1. Call check_weather.
2. Call get_wardrobe_items.
3. Recommend ONLY items that exist in the wardrobe.
4. If a recommended item is dirty, call wash_clothing for it before answering.
Never claim you performed an action unless you called the tool for it.
Never ask for permission — act.
"""

MAX_ITERATIONS = 10
MODEL_NAME = "qwen2.5:7b"

def run_agent_loop(context) -> tuple[str, list]:
    iteration_number = 0
    while iteration_number < MAX_ITERATIONS:
        response = client.responses.create(
            model=MODEL_NAME,
            instructions=SYSTEM_PROMPT,
            input=context,
            tools=TOOLS_REGISTRY,
            max_output_tokens=500,
            parallel_tool_calls=False,
        )
        item_names = [type(item).__name__ for item in response.output]
        print(f"[THINK]: Model decided to return these items: {item_names}")

        context += response.output

        for item in response.output:
            if item.type == "function_call":
                try:
                    func = TOOL_NAME_TO_FUNC[item.name]
                    args = json.loads(item.arguments)
                    tool_result = func(**args)
                except Exception as e:
                    tool_result = f"ERROR: {type(e).__name__}: {e}"
                print(f'[ACT]: Calling "{item.name}" with arguments {item.arguments}')

                context.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": tool_result,
                })
                print(f"[OBSERVE]: Result {tool_result}")

            if item.type == "message":
                return item.content[0].text, context

        iteration_number += 1

    return "Agent didn't finish in time", context

def main():
    context = []

    while True:
        input_message = input("[USER]: ").strip()
        if input_message.lower() in ["q", "quit", "exit"]:
            return
        context.append({"role": "user", "content": input_message})

        print("[ENTERING AGENT LOOP]")
        response, context = run_agent_loop(context)
        print("[EXITING AGENT LOOP]")
        print(f"[ASSISTANT]: {response}")


if __name__ == "__main__":
    main()
