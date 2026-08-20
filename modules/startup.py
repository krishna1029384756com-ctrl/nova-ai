"""
NOVA AI
Central Startup System
"""

import threading
import time

from modules.server import create_server
from modules import tray
from modules import window

from internet import (
    check_internet,
    get_internet_status
)


def start_nova():

    print("=" * 50)
    print("           NOVA AI")
    print("=" * 50)

    # ========================================================
    # CONFIGURATION
    # ========================================================

    print("[1/6] Loading Configuration...")

    # ========================================================
    # MEMORY
    # ========================================================

    print("[2/6] Loading Memory...")

    # ========================================================
    # BRAIN
    # ========================================================

    print("[3/6] Loading Brain...")

    # ========================================================
    # INTERNET
    # ========================================================

    print("[4/6] Loading Internet...")

    if check_internet():

        print(
            "      🌐 Internet connection detected."
        )

    else:

        print(
            "      ⚠️ Internet connection unavailable."
        )

    # ========================================================
    # ROUTES
    # ========================================================

    print("[5/6] Loading Routes...")

    # ========================================================
    # SERVER
    # ========================================================

    print("[6/6] Starting Server...")

    app = create_server()

    server_thread = threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        ),
        daemon=True
    )

    server_thread.start()

    # ========================================================
    # TRAY
    # ========================================================

    tray_thread = threading.Thread(
        target=tray.start,
        daemon=True
    )

    tray_thread.start()

    # ========================================================
    # WINDOW STATUS
    # ========================================================

    def _mark_online():

        time.sleep(0.5)

        window.update_status(
            "Online"
        )

    threading.Thread(
        target=_mark_online,
        daemon=True
    ).start()

    # ========================================================
    # STARTUP COMPLETE
    # ========================================================

    print()
    print("=" * 40)

    print(
        "NOVA Backend is Online"
    )

    print(
        "Version : 0.3"
    )

    print(
        f"Internet: {get_internet_status()}"
    )

    print(
        "Running in the background."
    )

    print(
        "Check your system tray."
    )

    print(
        "Right-click the tray icon "
        "to open chat or exit."
    )

    print("=" * 40)
    print()

    # ========================================================
    # KEEP NOVA ALIVE
    # ========================================================

    window.start(
        start_hidden=True
    )


if __name__ == "__main__":
    start_nova()