import json
import os
from datetime import datetime

# Installed NOVA runs from Program Files, so user-writable data belongs in
# the current user's AppData folder rather than beside the application files.
APP_DATA_DIR = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "NOVA AI")
MEMORY_FILE = os.path.join(APP_DATA_DIR, "memory.json")
MAX_HISTORY = 200


def _load():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {"history": []}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"history": []}


def _save(data):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
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
