import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No GOOGLE_API_KEY found.")
    exit()

genai.configure(api_key=api_key)

with open("available_models_log.txt", "w") as f:
    f.write("--- AVAILABLE MODELS ---\n")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"Name: {m.name}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")
    f.write("--- END ---\n")
