import threading

import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

# pyttsx3's engine isn't safe to drive from multiple threads at once,
# so we serialize calls with a lock (routes.py fires speak() in a
# background thread so it doesn't block the HTTP response).
_lock = threading.Lock()


def speak(text):
    print(f"NOVA: {text}")
    with _lock:
        engine.say(text)
        engine.runAndWait()
