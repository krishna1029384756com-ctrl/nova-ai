import threading
import time

from modules.server import create_server
from modules import tray
from modules import window
from modules.version import __version__


def start_nova():
    print("=" * 50)
    print("           NOVA AI")
    print("=" * 50)
    print("[1/5] Loading Configuration...")
    print("[2/5] Loading Memory...")
    print("[3/5] Loading Brain...")
    print("[4/5] Loading Routes...")
    print("[5/5] Starting Server...")

    app = create_server()
    server_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False),
        daemon=True,
    )
    server_thread.start()

    tray_thread = threading.Thread(target=tray.start, daemon=True)
    tray_thread.start()

    def _mark_online():
        time.sleep(0.5)
        window.update_status("Online")

    threading.Thread(target=_mark_online, daemon=True).start()

    print("\n========================================")
    print("NOVA Backend is Online")
    print(f"Version : {__version__}")
    print("Running in the background — check your system tray.")
    print("========================================\n")

    window.start(start_hidden=True)


if __name__ == "__main__":
    start_nova()
