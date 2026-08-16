"""
NOVA Desktop App - Entry point for PyInstaller
"""
import sys
import os
import threading
import time
import webview
from modules.server import create_server

# ─── Fix paths when running as bundled exe ───
if getattr(sys, 'frozen', False):
    # Running as compiled .exe
    BASE_DIR = sys._MEIPASS
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Flask server runner ───
def start_flask():
    # Tell Flask where the frontend is (relative to the bundled location)
    from flask import Flask
    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, 'frontend'),
        static_url_path=''
    )
    # Register routes (we import routes from modules)
    from modules.routes import register_routes
    register_routes(app)
    # Run the server
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

# ─── Open desktop window ───
def main():
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    time.sleep(1.5)  # wait for server to start

    # Create native window
    window = webview.create_window(
        title="NOVA AI",
        url="http://127.0.0.1:5000",
        width=1024,
        height=720,
        resizable=True,
        min_size=(640, 480),
        confirm_close=True,
        text_select=True,
    )
    webview.start(window, debug=False)

if __name__ == "__main__":
    main()