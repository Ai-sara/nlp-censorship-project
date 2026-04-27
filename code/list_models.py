from google import genai

client = genai.Client(api_key="AIzaSyAQhHU1odDOGWQG8Mt9_hfPQylLMkraplE")

for model in client.models.list():
    print(model.name)