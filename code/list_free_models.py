import requests

API_KEY = "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"

headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
models = response.json()["data"]

free_models = [m["id"] for m in models if ":free" in m["id"]]
for m in free_models:
    print(m)