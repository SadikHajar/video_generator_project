import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# Test the API key
api_key = os.getenv("LITELLM_API_KEY")
model = os.getenv("LITELLM_MODEL")

print(f"API Key loaded: {'Yes' if api_key else 'No'}")
print(f"Model: {model}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Set Google API key for Gemini
if model and model.startswith("gemini/"):
    os.environ["GOOGLE_API_KEY"] = api_key
    print("✅ GOOGLE_API_KEY set for Gemini model")

# Test a simple completion
try:
    response = completion(
        model=model,
        messages=[
            {"role": "user", "content": "Hello, just say 'Hi' back"}
        ],
        max_tokens=10
    )
    print("✅ API test successful!")
    print(f"Response: {response['choices'][0]['message']['content']}")
except Exception as e:
    print(f"❌ API test failed: {e}")
