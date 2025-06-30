from openai import OpenAI
from dotenv import load_dotenv
import os
from openai import OpenAI
import json

print("... Starting OpenRouter.py ...")  ##########

with open("config.json", "r") as f:
    config = json.load(f)
print("[DEBUG] config loaded :)")  #############

load_dotenv()
print("[DEBUG] dotenv loaded :D")  #############

ENV_KEY = os.environ.get("OPENROUTER_API_KEY")


client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=ENV_KEY)
print("[DEBUG] OpenAI called :)")
completion = client.chat.completions.create(
    model=config[0]["model"],
    max_tokens=config[0]["max_tokens"],
    temperature=config[0]["temperature"],
    messages=[
        {"role": "system", "content": "You are a helpful and attencious assistant."},
        {"role": "user", "content": input("What do you want to ask the AI? ")},
    ],
)
print("[DEBUG] answer received :D")

print(completion.choices[0].message.content)
print("script complete")
