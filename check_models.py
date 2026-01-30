import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

candidates = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-001",
    "models/gemini-1.5-pro",
    "models/gemini-pro",
    "models/gemini-1.0-pro",
    "models/gemini-2.0-flash-exp",
]

print("Checking models...")
try:
    available_models = [m.name for m in genai.list_models()]
    for cand in candidates:
        if cand in available_models:
            print(f"FOUND: {cand}")
        else:
            print(f"MISSING: {cand}")
            
    print("\nFirst 5 available models:")
    for m in available_models[:5]:
        print(m)
        
except Exception as e:
    print(f"Error: {e}")
