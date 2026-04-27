from google import genai

client = genai.Client(api_key="AIzaSyAQhHU1odDOGWQG8Mt9_hfPQylLMkraplE")

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="What is photosynthesis?"
)

print(response.text)