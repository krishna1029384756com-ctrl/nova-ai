import os
import webbrowser

import pystray
from PIL import Image, ImageDraw

from modules import window

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


def exit_program(icon, item):
    icon.stop()
    # Hard-stop the whole process (Flask thread + Tkinter mainloop included).
    # Fine for a personal local assistant; keeps shutdown simple and reliable.
    os._exit(0)


def start():
    global icon

    menu = pystray.Menu(
        pystray.MenuItem("Open Chat", open_chat, default=True),
        pystray.MenuItem("Show Status Window", show_status_window),
        pystray.MenuItem("Exit", exit_program)
    )

    icon = pystray.Icon("NOVA", create_image(), "NOVA", menu)
    icon.run()
