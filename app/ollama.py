import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma4",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]