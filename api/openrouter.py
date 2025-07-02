from openai import OpenAI
import json
import os

print("... Starting OpenRouter.py ...")  #############   Loads JSON strings

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), ".", "settings.json")
with open(os.path.abspath(SETTINGS_PATH), "r") as f:
    settings = json.load(f)
model = settings[0]["model"]
temperature = settings[0]["temperature"]
max_tokens = settings[0]["max_tokens"]
print(
    f"[DEBUG] settings loaded:\n model={model},\n temperature={temperature},\n max_tokens={max_tokens} :D"
)  #############
print("[DEBUG] settings json loaded :)")  #############


class OpenRouter:                         #############  Class for OpenRouter methods
    def __init__(self, base_url, api_key):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        print("[DEBUG] OpenRouter called :)")
        
    def chat_completion(self, messages):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            plugins=
            
        )
        
        return response


print("[DEBUG] ... OpenRouter.py End ...")  #############
