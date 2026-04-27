from huggingface_hub import InferenceClient

client = InferenceClient(token="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")

response = client.chat_completion(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[{"role": "user", "content": "What is photosynthesis?"}],
    max_tokens=100,
)

print(response.choices[0].message["content"])