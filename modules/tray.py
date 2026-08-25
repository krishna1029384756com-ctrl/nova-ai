import os
import threading
import webbrowser

import pystray
from PIL import Image, ImageDraw

from modules import updater, window

icon = None


def create_image():
    image = Image.new("RGB", (64, 64), (0, 120, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((12, 12, 52, 52), fill="white")
    return image


def open_chat(icon, item):
    webbrowser.open("http://localhost:5000")


def show_status_window(icon, item):
    window.show()


def _check_for_updates(icon, item):
    def worker():
        try:
            update = updater.check_for_update()
            if not update:
                window.notify("NOVA AI", "You are already using the latest version.")
                return

            window.notify(
                "NOVA AI update available",
                f"Version {update['version']} is available. Starting the update...",
            )
            updater.install_update(update)
            icon.stop()
            os._exit(0)
        except Exception as exc:
            window.notify("NOVA AI update failed", str(exc))

    threading.Thread(target=worker, daemon=True).start()


def exit_program(icon, item):
    icon.stop()
    os._exit(0)


def start():
    global icon
    menu = pystray.Menu(
        pystray.MenuItem("Open Chat", open_chat, default=True),
        pystray.MenuItem("Show Status Window", show_status_window),
        pystray.MenuItem("Check for Updates", _check_for_updates),
        pystray.MenuItem("Exit", exit_program),
    )
    icon = pystray.Icon("NOVA", create_image(), "NOVA", menu)
    icon.run()
