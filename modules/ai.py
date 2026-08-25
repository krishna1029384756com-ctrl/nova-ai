import os
import re
import importlib.util

import requests

import config
from modules import model_manager


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


_local_llm = None


def _get_local_llm():
    global _local_llm
    if _local_llm is None:
        from llama_cpp import Llama

        # First installed run downloads the model into AppData. Later app
        # updates keep the same model because it is outside Program Files.
        model_path = model_manager.ensure_model()
        print(f"[AI] Loading local model from {model_path}...")
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
    return _strip_thinking(result["choices"][0]["message"]["content"].strip())


def switch_local_model(model_path):
    global _local_llm
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    _local_llm = None
    config.LOCAL_MODEL_PATH = model_path
    _get_local_llm()


def _generate_ollama_reply(messages):
    response = requests.post(
        config.OLLAMA_URL,
        json={"model": config.OLLAMA_MODEL, "messages": messages, "stream": False},
        timeout=config.OLLAMA_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["message"]["content"].strip()


def _generate_openai_reply(messages):
    if not config.OPENAI_API_KEY:
        raise RuntimeError("No OpenAI API key configured")
    response = requests.post(
        config.OPENAI_URL,
        headers={"Authorization": f"Bearer {config.OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={"model": config.OPENAI_MODEL, "messages": messages},
        timeout=config.OPENAI_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _generate_grok_reply(messages):
    if not config.GROK_API_KEY:
        raise RuntimeError("No Grok API key configured")
    response = requests.post(
        config.GROK_URL,
        headers={"Authorization": f"Bearer {config.GROK_API_KEY}", "Content-Type": "application/json"},
        json={"model": config.GROK_MODEL, "messages": messages, "stream": False},
        timeout=config.GROK_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


_PROVIDERS = {
    "local": _generate_local_reply,
    "ollama": _generate_ollama_reply,
    "openai": _generate_openai_reply,
    "grok": _generate_grok_reply,
}


def generate_reply(user_message, history=None):
    messages = _build_messages(user_message, history or [])
    return _PROVIDERS.get(config.AI_PROVIDER, _generate_local_reply)(messages)


def is_available():
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
