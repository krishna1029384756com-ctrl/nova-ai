# NOVA configuration

# --- AI provider switch ---
# "local"  = free, fully offline, runs INSIDE NOVA itself via llama.cpp - no
#            separate app/service needed (unlike Ollama)
# "grok"   = xAI's Grok, costs a small amount per message, needs an API key
# "openai" = OpenAI, costs a small amount per message, needs an API key
# "ollama" = free, runs on your PC, needs a separate Ollama app installed and running
AI_PROVIDER = "local"

# --- Local AI (llama.cpp, embedded directly - no external app) ---
# 1. pip install -r requirements.txt   (installs llama-cpp-python)
# 2. Download the model file (~1.1 GB) and save it at the path below:
#    https://huggingface.co/unsloth/Qwen3-1.7B-GGUF/resolve/main/Qwen3-1.7B-Q4_K_M.gguf
#    Put it in a "models" folder inside the novaAI project folder.
LOCAL_MODEL_PATH = "models/Qwen3-1.7B-Q4_K_M.gguf"
LOCAL_CONTEXT_SIZE = 4096     # how many tokens of context the model can see at once
LOCAL_MAX_TOKENS = 200        # max length of a single reply
LOCAL_THREADS = None          # None = let llama.cpp auto-detect CPU threads

AI_HISTORY_LENGTH = 6        # how many past exchanges to give the AI as context

# --- Grok (xAI) ---
# Get a key from https://console.x.ai/team/default/api-keys (needs billing/credits set up).
# NEVER share this file or upload it publicly once a real key is pasted in.
GROK_API_KEY = ""            # paste your key between the quotes, e.g. "xai-..."
GROK_MODEL = "grok-4.5"      # xAI's current flagship model as of Aug 2026
GROK_URL = "https://api.x.ai/v1/chat/completions"
GROK_TIMEOUT = 30

# --- Local AI (Ollama) ---
# Ollama must be installed and running separately: https://ollama.com
# After installing, pull a model once from a terminal, e.g.:
#   ollama pull llama3.2
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:1b"
OLLAMA_TIMEOUT = 30          # seconds to wait for a reply before giving up

# --- OpenAI API ---
# Get a key from https://platform.openai.com/api-keys (needs billing set up).
# NEVER share this file or upload it publicly once a real key is pasted in.
OPENAI_API_KEY = ""          # paste your key between the quotes, e.g. "sk-..."
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
