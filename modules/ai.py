import requests

import config


def _build_messages(user_message, history):
    messages = [{"role": "system", "content": config.AI_SYSTEM_PROMPT}]

    for exchange in history:
        messages.append({"role": "user", "content": exchange["message"]})
        messages.append({"role": "assistant", "content": exchange["reply"]})

    messages.append({"role": "user", "content": user_message})
    return messages


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


def generate_reply(user_message, history=None):
    """
    Calls whichever AI provider is set in config.AI_PROVIDER ("ollama" or
    "openai") for a real AI-generated reply.

    Raises an exception (connection error, timeout, missing API key, etc.)
    if the provider isn't reachable/configured - brain.py catches this and
    falls back to basic rule-based replies so NOVA still responds either way.
    """
    messages = _build_messages(user_message, history or [])

    if config.AI_PROVIDER == "openai":
        return _generate_openai_reply(messages)
    return _generate_ollama_reply(messages)


def is_available():
    """Quick check for whether the configured AI provider is actually usable
    right now (used by the frontend to show 'AI Ready' vs 'Basic Mode')."""
    if config.AI_PROVIDER == "openai":
        return bool(config.OPENAI_API_KEY)

    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except requests.RequestException:
        return False
