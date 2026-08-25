import os
from pathlib import Path

# --- Application data ---
# Installed files live under Program Files, so writable user data belongs in AppData.
APP_DATA_DIR = Path(os.getenv("APPDATA", Path.home())) / "NOVA AI"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR = APP_DATA_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# --- AI provider switch ---
# "local"  = free, fully offline after the model is downloaded, runs inside NOVA
# "grok"   = xAI's Grok, needs an API key
# "openai" = OpenAI, needs an API key
# "ollama" = free, runs on your PC, needs Ollama installed and running
AI_PROVIDER = "local"

# --- Local AI (llama.cpp, embedded directly) ---
# NOVA downloads this model automatically on first use into AppData.
LOCAL_MODEL_FILENAME = "Qwen3-1.7B-Q4_K_M.gguf"
LOCAL_MODEL_PATH = str(MODEL_DIR / LOCAL_MODEL_FILENAME)
LOCAL_MODEL_URL = (
    "https://huggingface.co/ggml-org/Qwen3-1.7B-GGUF/resolve/main/"
    "Qwen3-1.7B-Q4_K_M.gguf?download=true"
)
LOCAL_MODEL_SHA256 = "d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
LOCAL_CONTEXT_SIZE = 4096
LOCAL_MAX_TOKENS = 200
LOCAL_THREADS = None

AI_HISTORY_LENGTH = 6

# --- Updates ---
GITHUB_REPOSITORY = "krishna1029384756com-ctrl/nova-ai"
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases/latest"

# --- Grok (xAI) ---
GROK_API_KEY = ""
GROK_MODEL = "grok-4.5"
GROK_URL = "https://api.x.ai/v1/chat/completions"
GROK_TIMEOUT = 30

# --- Local AI (Ollama) ---
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:1b"
OLLAMA_TIMEOUT = 30

# --- OpenAI API ---
OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TIMEOUT = 30

AI_SYSTEM_PROMPT = (
    "You are NOVA, a personal AI assistant running locally on Krishna's laptop. "
    "Keep replies short and conversational (1-3 sentences) since they are often "
    "read aloud with text-to-speech. Be direct and helpful. You don't control "
    "the PC yourself through this chat - app launching and web search are "
    "handled separately - so just have a normal, friendly conversation."
)
