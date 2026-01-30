import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
]

print("--- Testing Model Quotas ---")
for model_name in candidates:
    print(f"Testing: {model_name}...", end=" ")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi", request_options={'timeout': 10})
        print(f"✅ SUCCESS")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ NOT FOUND")
        elif "429" in error_msg:
            print(f"❌ QUOTA EXCEEDED / RATE LIMIT")
        else:
            print(f"❌ ERROR: {error_msg[:50]}...")
    time.sleep(1) # Be debugging nice
