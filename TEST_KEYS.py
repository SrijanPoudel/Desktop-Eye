import os
from dotenv import load_dotenv

load_dotenv('/Users/macbook/Desktop/ai_ml_chatbot/.env', override=True)

openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    print(f"✅ OpenAI key loaded: {openai_key[:8]}...  ✓")
    print("You're ready to build!")
else:
    print("❌ Still not loading")
