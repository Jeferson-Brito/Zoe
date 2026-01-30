import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    print("\n--- Testing Gemini API ---")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY missing from .env")
        return
    
    genai.configure(api_key=api_key)
    model_name = "gemini-1.5-flash"
    print(f"Testing Model: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"✅ SUCCESS! Response: {response.text.strip()[:20]}...")
    except Exception as e:
        print(f"❌ FAILED: {e}")

def test_server():
    print("\n--- Testing Local Server (Port 8000) ---")
    try:
        r = requests.get("http://127.0.0.1:8000/")
        print(f"✅ Server is UP! Status Code: {r.status_code}")
    except Exception as e:
        print(f"❌ Server Connection FAILED: {e}")
        print("   (Did you run `run_server.bat`?)")

if __name__ == "__main__":
    test_gemini()
    test_server()
