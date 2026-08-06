# NOVA configuration

# --- AI provider switch ---
# "ollama" = free, runs on your PC, needs Ollama installed and running
# "openai" = costs a small amount per message, needs an API key, no local setup
AI_PROVIDER = "ollama"

# --- Local AI (Ollama) ---
# Ollama must be installed and running separately: https://ollama.com
# After installing, pull a model once from a terminal, e.g.:
#   ollama pull llama3.2
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:1b"
OLLAMA_TIMEOUT = 30          # seconds to wait for a reply before giving up
AI_HISTORY_LENGTH = 6        # how many past exchanges to give the AI as context

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
