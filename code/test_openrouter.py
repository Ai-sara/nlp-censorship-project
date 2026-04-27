import requests

API_KEY = "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"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-oss-20b:free",
    "messages": [{"role": "user", "content": "What is photosynthesis?"}]
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=payload
)

print(response.status_code)
print(response.json())