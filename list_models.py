import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# List all available models
for m in genai.list_models():
    print(f"Model: {m.name}")
    print(f"Display name: {m.display_name}")
    print(f"Description: {m.description}")
    print(f"Generation methods: {m.supported_generation_methods}")
    print("-" * 50) 