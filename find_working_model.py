import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def test_models():
    print("--- BRUTE FORCE MODEL CHECK ---")
    
    # Get all models from API
    all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # Priority list (try these first)
    priority = [
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "models/gemini-1.0-pro",
        "models/gemini-pro",
    ]
    
    # Combine (priority first, then unique others)
    candidates = priority + [m for m in all_models if m not in priority]
    
    for model_name in candidates:
        # Strip 'models/' prefix if needed for instantiation, but typically genai accepts both
        short_name = model_name.replace("models/", "")
        print(f"Testing: {short_name: <30}", end=" ")
        
        try:
            model = genai.GenerativeModel(short_name)
            response = model.generate_content("Hi", request_options={'timeout': 5})
            print(f"✅ SUCCESS! Response: {response.text.strip()[:10]}...")
            print(f"\n🎉 FOUND WORKING MODEL: {short_name}")
            return short_name
        except Exception as e:
            err = str(e)
            if "404" in err:
                 print("❌ Not Found")
            elif "429" in err:
                 print("❌ Quota Exceeded")
            else:
                 print(f"❌ Error: {err[:20]}...")
        
        time.sleep(0.5)

    print("\n💀 ALL MODELS FAILED. No quota or access remaining.")
    return None

if __name__ == "__main__":
    test_models()
