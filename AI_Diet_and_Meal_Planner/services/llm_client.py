import os
from dotenv import load_dotenv
from typing import Any
import requests
import json

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.api_url = f"{self.base_url}/chat/completions"
        self.model = os.getenv("OPENAI_MODEL")

    def call_model_json(self, prompt: str) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        body = {
            "model": self.model,
            "messages": [
                {
                "role": "user",
                "content": prompt,
                }
            ],
            "response_format": {"type": "json_object"}
        }

        response = requests.post(url=self.api_url, headers=headers, json=body, timeout=60)
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        result = json.loads(text)
        return result