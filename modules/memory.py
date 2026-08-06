import json
import os
from datetime import datetime

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "memory.json")
MAX_HISTORY = 200


def _load():
    try:
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {"history": []}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"history": []}


def _save(data):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_exchange(message, reply):
    data = _load()
    data["history"].append({
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "reply": reply,
    })
    data["history"] = data["history"][-MAX_HISTORY:]
    _save(data)


def get_history(limit=20):
    data = _load()
    return data["history"][-limit:]


def clear_history():
    _save({"history": []})
