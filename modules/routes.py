import threading

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

        # Speak the reply out loud without blocking the HTTP response
        threading.Thread(target=voice.speak, args=(reply,), daemon=True).start()

        # Keep the desktop status window in sync with the latest reply
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
    # The browser's wake-word listener (app.js) posts here at key moments
    # so the desktop status window can visibly reflect what's happening -
    # useful both for the "Jarvis" feel and for debugging: if this window
    # never updates, the browser-side listener isn't reaching this endpoint.

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
