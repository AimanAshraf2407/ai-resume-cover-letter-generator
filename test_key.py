import os
from dotenv import load_dotenv
from google import genai

# Load API key from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Checking API Key: {api_key[:6]}... (Length: {len(api_key) if api_key else 0})")

if not api_key:
    print("❌ ERROR: No API key found. Check your .env file!")
    exit(1)

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say 'API key is working!' in 5 words or less.",
    )
    print("✅ SUCCESS! The Gemini API key is valid.")
    print("Response from Gemini:", response.text)

except Exception as e:
    print("❌ FAILED! Key is invalid or there is an issue with the request.")
    print("Error details:", e)