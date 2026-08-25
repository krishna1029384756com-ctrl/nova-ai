"""NOVA AI central startup system."""

import os
import sys
import threading
import time

from modules.server import create_server
from modules import tray, window
from modules.version import __version__
from internet import check_internet, get_internet_status

STARTUP_FUNCTIONS = {}


def register_function(number, name, function):
    STARTUP_FUNCTIONS[number] = {"name": name, "function": function}


def load_settings():
    print("[1/6] Loading Settings...")


def load_memory():
    print("[2/6] Loading Memory...")


def load_brain():
    print("[3/6] Loading Brain...")


def load_internet():
    print("[4/6] Loading Internet...")
    print(f"      Status: {get_internet_status()}")


def load_website():
    print("[5/6] Loading Website...")


def load_server():
    print("[6/6] Starting Server...")
    app = create_server()
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False),
        daemon=True,
    ).start()
    threading.Thread(target=tray.start, daemon=True).start()

    def mark_online():
        time.sleep(0.5)
        try:
            window.update_status("Online")
        except Exception as error:
            print(f"NOVA WINDOW ERROR: {error}")

    threading.Thread(target=mark_online, daemon=True).start()


register_function(1, "Settings", load_settings)
register_function(2, "Memory", load_memory)
register_function(3, "Brain", load_brain)
register_function(4, "Internet", load_internet)
register_function(5, "Website", load_website)
register_function(6, "Server", load_server)


def restart_function():
    print("\nNOVA STARTUP FUNCTIONS")
    for number, data in STARTUP_FUNCTIONS.items():
        print(f"{number}. {data['name']}")
    choice = input("Which function do you want to restart? ").strip()
    if not choice.isdigit() or int(choice) not in STARTUP_FUNCTIONS:
        print("NOVA: Function not found.")
        return
    data = STARTUP_FUNCTIONS[int(choice)]
    try:
        data["function"]()
        print(f"NOVA: {data['name']} restarted successfully.")
    except Exception as error:
        print(f"NOVA ERROR: {error}")


def restart_all():
    os.execl(sys.executable, sys.executable, *sys.argv)


def startup_command_listener():
    while True:
        try:
            command = input("NOVA > ").strip().lower()
            if command == "r":
                restart_function()
            elif command == "ra":
                restart_all()
            else:
                print("NOVA: Use r = restart function, ra = restart NOVA")
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as error:
            print(f"NOVA CONTROL ERROR: {error}")


def start_nova():
    print("=" * 50)
    print("           NOVA AI")
    print("=" * 50)
    load_settings()
    load_memory()
    load_brain()
    load_internet()
    load_website()
    load_server()
    print("\nNOVA Backend is Online")
    print(f"Version : {__version__}")
    print("Controls: r = restart function, ra = restart NOVA")
    threading.Thread(target=startup_command_listener, daemon=True).start()
    window.start(start_hidden=True)


if __name__ == "__main__":
    start_nova()
