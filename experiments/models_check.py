# models_check.py — créalo en la raíz y ejecútalo
import os
from dotenv import load_dotenv
import requests


load_dotenv()
response = requests.get(
    "https://api.fireworks.ai/inference/v1/models",
    headers={"Authorization": f"Bearer {os.getenv('FIREWORKS_API_KEY')}"}
)

models = response.json()
for m in models.get("data", []):
    print(m["id"])