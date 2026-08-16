import os
import re
import importlib.util

import requests

import config


def _build_messages(user_message, history):
    system_prompt = config.AI_SYSTEM_PROMPT

    if config.AI_PROVIDER == "local":
        system_prompt += " /no_think"

    messages = [{"role": "system", "content": system_prompt}]

    for exchange in history:
        messages.append({"role": "user", "content": exchange["message"]})
        messages.append({"role": "assistant", "content": exchange["reply"]})

    messages.append({"role": "user", "content": user_message})
    return messages


def _strip_thinking(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# =========================
# Local (llama.cpp, embedded)
# =========================

_local_llm = None


def _get_local_llm():
    global _local_llm
    if _local_llm is None:
        from llama_cpp import Llama

        if not os.path.isfile(config.LOCAL_MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at '{config.LOCAL_MODEL_PATH}'. "
                f"Download it and place it there - see config.py for the link."
            )

        print(f"[AI] Loading local model from {config.LOCAL_MODEL_PATH} (first message will be slower)...")
        _local_llm = Llama(
            model_path=config.LOCAL_MODEL_PATH,
            n_ctx=config.LOCAL_CONTEXT_SIZE,
            n_threads=config.LOCAL_THREADS,
            verbose=False,
        )
    return _local_llm


def _generate_local_reply(messages):
    llm = _get_local_llm()
    result = llm.create_chat_completion(
        messages=messages,
        max_tokens=config.LOCAL_MAX_TOKENS,
        temperature=0.7,
    )
    text = result["choices"][0]["message"]["content"].strip()
    return _strip_thinking(text)


# =========================
# NEW: Hot‑swap model without restart
# =========================

def switch_local_model(model_path):
    """
    Dynamically reload the local model with a new GGUF file.
    Call this instead of restarting the server.
    """
    global _local_llm

    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # Unload current model
    _local_llm = None

    # Update config path so future loads use the new file
    config.LOCAL_MODEL_PATH = model_path

    # Force a fresh load
    _get_local_llm()

    print(f"[AI] Switched to model: {model_path}")


# =========================
# Ollama (optional)
# =========================

def _generate_ollama_reply(messages):
    response = requests.post(
        config.OLLAMA_URL,
        json={
            "model": config.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
        },
        timeout=config.OLLAMA_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"].strip()


# =========================
# OpenAI (optional)
# =========================

def _generate_openai_reply(messages):
    if not config.OPENAI_API_KEY:
        raise RuntimeError("No OpenAI API key set in config.py (OPENAI_API_KEY is empty)")

    response = requests.post(
        config.OPENAI_URL,
        headers={
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.OPENAI_MODEL,
            "messages": messages,
        },
        timeout=config.OPENAI_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


# =========================
# Grok (optional)
# =========================

def _generate_grok_reply(messages):
    if not config.GROK_API_KEY:
        raise RuntimeError("No Grok API key set in config.py (GROK_API_KEY is empty)")

    response = requests.post(
        config.GROK_URL,
        headers={
            "Authorization": f"Bearer {config.GROK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.GROK_MODEL,
            "messages": messages,
            "stream": False,
        },
        timeout=config.GROK_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


# =========================
# Dispatch
# =========================

_PROVIDERS = {
    "local": _generate_local_reply,
    "ollama": _generate_ollama_reply,
    "openai": _generate_openai_reply,
    "grok": _generate_grok_reply,
}


def generate_reply(user_message, history=None):
    """
    Calls whichever AI provider is set in config.AI_PROVIDER for a real
    AI-generated reply.
    """
    messages = _build_messages(user_message, history or [])
    generator = _PROVIDERS.get(config.AI_PROVIDER, _generate_local_reply)
    return generator(messages)


def is_available():
    """Quick check if the configured AI provider is usable."""
    if config.AI_PROVIDER == "local":
        has_package = importlib.util.find_spec("llama_cpp") is not None
        has_model = os.path.isfile(config.LOCAL_MODEL_PATH)
        return has_package and has_model

    if config.AI_PROVIDER == "openai":
        return bool(config.OPENAI_API_KEY)

    if config.AI_PROVIDER == "grok":
        return bool(config.GROK_API_KEY)

    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except requests.RequestException:
        return False