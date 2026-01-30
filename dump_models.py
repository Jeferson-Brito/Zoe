import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

with open("all_models.txt", "w", encoding="utf-8") as f:
    try:
        f.write("--- Available Models ---\n")
        for m in genai.list_models():
            f.write(f"Name: {m.name}\n")
            f.write(f"Methods: {m.supported_generation_methods}\n")
            f.write("-" * 20 + "\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
