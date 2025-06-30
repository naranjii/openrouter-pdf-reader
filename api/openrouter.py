from openai import OpenAI
from dotenv import load_dotenv
import json
import os

print("... Starting OpenRouter.py ...")  #############

with open("settings.json", "r") as f:
    settings = json.load(f)
print("[DEBUG] settings json loaded :)")  #############

load_dotenv()
ENV_KEY = os.environ.get("OPENROUTER_API_KEY")
print("[DEBUG] dotenv loaded :D")  #############

class OpenRouterClient:
    def __init__(self, base_url, api_key):
        self.client = OpenAI(base_url, api_key)
        self.settings = settings.get("model","temperature","max_tokens")
        print("[DEBUG] OpenRouter called :)")
        
    def chat_completion(self, messages):
        response = self.client.chat.completions.create(
            model=self.settings.get("model"),
            messages=messages,
            temperature=self.settings.get("temperature"),
            max_tokens=self.settings.get("max_tokens")
        )
        return response

print("[DEBUG] answer received :D")


print("# Script End")
