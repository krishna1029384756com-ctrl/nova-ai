import threading
import os

import config

from flask import jsonify
from flask import send_from_directory
from flask import request

from modules.brain import brain
from modules import memory
from modules import voice
from modules import window
from modules import emotion
from modules import ai


WAKE_EVENT_MESSAGES = {
    "listening": ("Listening for the wake word...", "👂 Listening"),
    "triggered": ("Heard the wake word - go ahead...", "✨ Woke up"),
    "awaiting": ("Waiting for your command...", "🎙️ Awaiting command"),
    "heard": ("Got it, thinking...", "✅ Got it"),
    "error": ("Voice recognition hit a snag.", "⚠️ Error"),
    "idle": ("Wake word turned off.", "😊 Happy"),
}


def register_routes(app):

    # =========================
    # Frontend
    # =========================

    @app.route("/")
    def home():
        return send_from_directory("../frontend", "index.html")

    # =========================
    # Startup API
    # =========================

    @app.route("/api/startup")
    def startup():
        return jsonify({
            "success": True,
            "name": "NOVA",
            "version": brain.version,
            "status": "online",
            "ai_available": ai.is_available()
        })

    # =========================
    # Status API
    # =========================

    @app.route("/api/status")
    def status():
        return jsonify({
            "status": "online"
        })

    # =========================
    # Chat API
    # =========================

    @app.route("/api/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        message = data.get("message", "")
        reply = brain.chat(message)

        threading.Thread(target=voice.speak, args=(reply,), daemon=True).start()
        window.update_message(reply)
        emotion.set_emotion("😊 Happy")
        window.update_emotion(emotion.get_emotion())

        return jsonify({
            "reply": reply
        })

    # =========================
    # Memory / History API
    # =========================

    @app.route("/api/history")
    def history():
        return jsonify({
            "history": memory.get_history(limit=50)
        })

    # =========================
    # Wake word event bridge
    # =========================

    @app.route("/api/wake-event", methods=["POST"])
    def wake_event():
        data = request.get_json(silent=True) or {}
        event_type = data.get("event", "")
        text = data.get("text", "")

        status_text, emotion_text = WAKE_EVENT_MESSAGES.get(event_type, (None, None))

        if status_text:
            display = f'{status_text} ("{text}")' if text and event_type == "error" else status_text
            window.update_message(display)

        if emotion_text:
            emotion.set_emotion(emotion_text)
            window.update_emotion(emotion_text)

        if event_type == "triggered":
            window.show()

        return jsonify({"ok": True})

    # =========================
    # List available local GGUF models
    # =========================

    @app.route("/api/models")
    def list_models():
        # Support both the repository's models/ folder and the writable
        # AppData model directory configured for installed NOVA builds.
        project_models_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "models")
        )
        configured_models_dir = os.path.abspath(str(config.MODEL_DIR))
        models = set()

        for models_dir in (project_models_dir, configured_models_dir):
            try:
                for filename in os.listdir(models_dir):
                    full_path = os.path.join(models_dir, filename)
                    if os.path.isfile(full_path) and filename.lower().endswith(".gguf"):
                        models.add(filename)
            except FileNotFoundError:
                continue
            except OSError:
                continue

        return jsonify({"models": sorted(models, key=str.casefold)})

    # =========================
    # Switch local GGUF model
    # =========================

    @app.route("/api/switch-model", methods=["POST"])
    def switch_model():
        data = request.get_json(silent=True) or {}
        filename = data.get("filename", "")

        # Accept only a plain GGUF filename, never a caller-supplied path.
        if (
            not isinstance(filename, str)
            or not filename.lower().endswith(".gguf")
            or filename in (".", "..")
            or os.path.basename(filename) != filename
        ):
            return jsonify({"success": False, "error": "Invalid model filename"}), 400

        project_models_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "models")
        )
        configured_models_dir = os.path.abspath(str(config.MODEL_DIR))
        model_path = None

        # Prefer models/ for files with duplicate names, then check AppData.
        for models_dir in (project_models_dir, configured_models_dir):
            candidate = os.path.join(models_dir, filename)
            if os.path.isfile(candidate):
                model_path = candidate
                break

        if model_path is None:
            return jsonify({
                "success": False,
                "error": "That model was not found. Refresh the model list and try again."
            }), 404

        try:
            ai.switch_local_model(model_path)
            return jsonify({"success": True, "message": f"Switched to {filename}"})
        except Exception as error:
            return jsonify({"success": False, "error": str(error)}), 500
