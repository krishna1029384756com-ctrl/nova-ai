import os
import re
import importlib.util

import requests

import config
from modules import model_manager


# ============================================================
# MESSAGE BUILDER
# ============================================================

def _build_messages(user_message, history):
    system_prompt = config.AI_SYSTEM_PROMPT

    if config.AI_PROVIDER == "local":
        system_prompt += " /no_think"

<<<<<<< Updated upstream
    messages = [{"role": "system", "content": system_prompt}]
    for exchange in history:
        messages.append({"role": "user", "content": exchange["message"]})
        messages.append({"role": "assistant", "content": exchange["reply"]})
    messages.append({"role": "user", "content": user_message})
=======
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    for exchange in history:
        messages.append(
            {
                "role": "user",
                "content": exchange["message"],
            }
        )

        messages.append(
            {
                "role": "assistant",
                "content": exchange["reply"],
            }
        )

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

>>>>>>> Stashed changes
    return messages


# ============================================================
# THINKING TAG CLEANUP
# ============================================================

def _strip_thinking(text):
    return re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL,
    ).strip()


<<<<<<< Updated upstream
=======
# ============================================================
# LOCAL AI - LLAMA.CPP
# ============================================================

>>>>>>> Stashed changes
_local_llm = None


def _get_local_llm():
    global _local_llm

    if _local_llm is None:
        from llama_cpp import Llama

<<<<<<< Updated upstream
        # First installed run downloads the model into AppData. Later app
        # updates keep the same model because it is outside Program Files.
        model_path = model_manager.ensure_model()
        print(f"[AI] Loading local model from {model_path}...")
=======
        if not os.path.isfile(config.LOCAL_MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at "
                f"'{config.LOCAL_MODEL_PATH}'. "
                f"Download it and place it there."
            )

        print(
            "[AI] Loading local model from "
            f"{config.LOCAL_MODEL_PATH}..."
        )

>>>>>>> Stashed changes
        _local_llm = Llama(
            model_path=model_path,
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
<<<<<<< Updated upstream
    return _strip_thinking(result["choices"][0]["message"]["content"].strip())


def switch_local_model(model_path):
=======

    text = result["choices"][0]["message"]["content"].strip()

    return _strip_thinking(text)


# ============================================================
# HOT-SWAP LOCAL MODEL
# ============================================================

def switch_local_model(model_path):
    """
    Dynamically switch to another GGUF model.
    """

>>>>>>> Stashed changes
    global _local_llm
    if not os.path.isfile(model_path):
<<<<<<< Updated upstream
        raise FileNotFoundError(f"Model file not found: {model_path}")
    _local_llm = None
    config.LOCAL_MODEL_PATH = model_path
    _get_local_llm()

=======
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    _local_llm = None

    config.LOCAL_MODEL_PATH = model_path

    _get_local_llm()

    print(
        f"[AI] Switched to model: {model_path}"
    )


# ============================================================
# OLLAMA
# ============================================================
>>>>>>> Stashed changes

def _generate_ollama_reply(messages):
    response = requests.post(
        config.OLLAMA_URL,
        json={"model": config.OLLAMA_MODEL, "messages": messages, "stream": False},
        timeout=config.OLLAMA_TIMEOUT,
    )

    response.raise_for_status()
<<<<<<< Updated upstream
    return response.json()["message"]["content"].strip()


def _generate_openai_reply(messages):
    if not config.OPENAI_API_KEY:
        raise RuntimeError("No OpenAI API key configured")
    response = requests.post(
        config.OPENAI_URL,
        headers={"Authorization": f"Bearer {config.OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={"model": config.OPENAI_MODEL, "messages": messages},
=======

    data = response.json()

    return data["message"]["content"].strip()


# ============================================================
# OPENAI
# ============================================================

def _generate_openai_reply(messages):
    if not config.OPENAI_API_KEY:
        raise RuntimeError(
            "No OpenAI API key set in config.py"
        )

    response = requests.post(
        config.OPENAI_URL,
        headers={
            "Authorization":
                f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type":
                "application/json",
        },
        json={
            "model": config.OPENAI_MODEL,
            "messages": messages,
        },
>>>>>>> Stashed changes
        timeout=config.OPENAI_TIMEOUT,
    )

    response.raise_for_status()
<<<<<<< Updated upstream
    return response.json()["choices"][0]["message"]["content"].strip()


def _generate_grok_reply(messages):
    if not config.GROK_API_KEY:
        raise RuntimeError("No Grok API key configured")
    response = requests.post(
        config.GROK_URL,
        headers={"Authorization": f"Bearer {config.GROK_API_KEY}", "Content-Type": "application/json"},
        json={"model": config.GROK_MODEL, "messages": messages, "stream": False},
=======

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


# ============================================================
# GROK
# ============================================================

def _generate_grok_reply(messages):
    if not config.GROK_API_KEY:
        raise RuntimeError(
            "No Grok API key set in config.py"
        )

    response = requests.post(
        config.GROK_URL,
        headers={
            "Authorization":
                f"Bearer {config.GROK_API_KEY}",
            "Content-Type":
                "application/json",
        },
        json={
            "model": config.GROK_MODEL,
            "messages": messages,
            "stream": False,
        },
>>>>>>> Stashed changes
        timeout=config.GROK_TIMEOUT,
    )

    response.raise_for_status()
<<<<<<< Updated upstream
    return response.json()["choices"][0]["message"]["content"].strip()


=======

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


# ============================================================
# PROVIDER DISPATCH
# ============================================================

>>>>>>> Stashed changes
_PROVIDERS = {
    "local": _generate_local_reply,
    "ollama": _generate_ollama_reply,
    "openai": _generate_openai_reply,
    "grok": _generate_grok_reply,
}


<<<<<<< Updated upstream
def generate_reply(user_message, history=None):
    messages = _build_messages(user_message, history or [])
    return _PROVIDERS.get(config.AI_PROVIDER, _generate_local_reply)(messages)
=======
# ============================================================
# RAW MESSAGE GENERATOR
# ============================================================

def generate_raw_messages(messages):
    """
    Generate a response from an already-built
    list of chat messages.

    Used by NOVA's tool-aware Brain.
    """

    if not isinstance(messages, list):
        raise TypeError(
            "messages must be a list"
        )

    generator = _PROVIDERS.get(
        config.AI_PROVIDER
    )

    if generator is None:
        raise RuntimeError(
            f"Unsupported AI provider: "
            f"{config.AI_PROVIDER}"
        )

    return generator(messages)
>>>>>>> Stashed changes


# ============================================================
# NORMAL REPLY
# ============================================================

def generate_reply(user_message, history=None):
    """
    Generate a normal AI reply.
    """

    messages = _build_messages(
        user_message,
        history or [],
    )

    return generate_raw_messages(messages)


# ============================================================
# AVAILABILITY CHECK
# ============================================================

def is_available():
<<<<<<< Updated upstream
    if config.AI_PROVIDER == "local":
        return importlib.util.find_spec("llama_cpp") is not None and model_manager.model_exists()
    if config.AI_PROVIDER == "openai":
        return bool(config.OPENAI_API_KEY)
    if config.AI_PROVIDER == "grok":
        return bool(config.GROK_API_KEY)
    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except requests.RequestException:
        return False
=======
    """
    Check whether the configured AI provider
    appears usable.
    """

    if config.AI_PROVIDER == "local":

        has_package = (
            importlib.util.find_spec(
                "llama_cpp"
            )
            is not None
        )

        has_model = os.path.isfile(
            config.LOCAL_MODEL_PATH
        )

        return has_package and has_model

    if config.AI_PROVIDER == "openai":
        return bool(
            config.OPENAI_API_KEY
        )

    if config.AI_PROVIDER == "grok":
        return bool(
            config.GROK_API_KEY
        )

    if config.AI_PROVIDER == "ollama":
        try:
            requests.get(
                "http://localhost:11434",
                timeout=2,
            )

            return True

        except requests.RequestException:
            return False

    return False
>>>>>>> Stashed changes
