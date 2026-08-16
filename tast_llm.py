# test_llm.py
import config
from modules import ai

try:
    print("Checking if LLM is available...")
    if ai.is_available():
        print("✅ Model file found and llama_cpp installed.")
        print("Generating test reply...")
        reply = ai.generate_reply("Hello, who are you?")
        print(f"🤖 Reply: {reply}")
    else:
        print("❌ LLM not available. Check:")
        print("  - Is the model file at:", config.LOCAL_MODEL_PATH)
        print("  - Is llama-cpp-python installed?")
except Exception as e:
    print(f"❌ Error: {e}")