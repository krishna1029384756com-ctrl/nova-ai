"""
NOVA AI
Central Startup System
"""

import os
import sys
import threading
import time

from modules.server import create_server
from modules import tray
from modules import window

from internet import (
    check_internet,
    get_internet_status
)


# ============================================================
# STARTUP FUNCTIONS
# ============================================================

STARTUP_FUNCTIONS = {}


def register_function(number, name, function):
    """
    Register a NOVA startup function.
    """

    STARTUP_FUNCTIONS[number] = {
        "name": name,
        "function": function
    }


# ============================================================
# RESTART ONE FUNCTION
# ============================================================

def restart_function():
    """
    Restart one selected startup function.
    """

    print()
    print("========================================")
    print("       NOVA STARTUP FUNCTIONS")
    print("========================================")

    for number, data in STARTUP_FUNCTIONS.items():

        print(
            f"{number}. {data['name']}"
        )

    print("========================================")

    choice = input(
        "Which function do you want to restart? "
    ).strip()

    if not choice.isdigit():

        print(
            "NOVA: Invalid function number."
        )

        return

    number = int(choice)

    if number not in STARTUP_FUNCTIONS:

        print(
            "NOVA: Function not found."
        )

        return

    function_data = STARTUP_FUNCTIONS[number]

    print()

    print(
        f"NOVA: Restarting "
        f"{function_data['name']}..."
    )

    try:

        function_data["function"]()

        print()

        print(
            f"NOVA: "
            f"{function_data['name']} "
            f"restarted successfully."
        )

    except Exception as error:

        print()

        print(
            f"NOVA ERROR: {error}"
        )


# ============================================================
# RESTART COMPLETE STARTUP
# ============================================================

def restart_all():
    """
    Restart the entire NOVA startup.
    """

    print()

    print(
        "NOVA: Restarting complete startup..."
    )

    time.sleep(0.5)

    python = sys.executable

    os.execl(
        python,
        python,
        *sys.argv
    )


# ============================================================
# STARTUP COMMAND LISTENER
# ============================================================

def startup_command_listener():
    """
    Startup commands:

    r  = restart one selected function
    ra = restart entire startup
    """

    while True:

        try:

            command = input(
                "NOVA > "
            ).strip().lower()

            # ------------------------------------------------
            # RESTART ONE FUNCTION
            # ------------------------------------------------

            if command == "r":

                restart_function()

            # ------------------------------------------------
            # RESTART EVERYTHING
            # ------------------------------------------------

            elif command == "ra":

                restart_all()

            # ------------------------------------------------
            # UNKNOWN COMMAND
            # ------------------------------------------------

            else:

                print(
                    "NOVA: Unknown command."
                )

                print(
                    "NOVA: Use:"
                )

                print(
                    "  r  = restart one function"
                )

                print(
                    "  ra = restart entire startup"
                )

        except KeyboardInterrupt:

            print()

            print(
                "NOVA: Command listener stopped."
            )

            break

        except EOFError:

            break

        except Exception as error:

            print(
                f"NOVA CONTROL ERROR: {error}"
            )


# ============================================================
# SETTINGS
# ============================================================

def load_settings():

    print(
        "[1/6] Loading Settings..."
    )


# ============================================================
# MEMORY
# ============================================================

def load_memory():

    print(
        "[2/6] Loading Memory..."
    )


# ============================================================
# BRAIN
# ============================================================

def load_brain():

    print(
        "[3/6] Loading Brain..."
    )


# ============================================================
# INTERNET
# ============================================================

def load_internet():

    print(
        "[4/6] Loading Internet..."
    )

    print(
        "      Checking real internet connection..."
    )

    try:

        online = check_internet()

        if online:

            print(
                "      🌐 Internet connection detected."
            )

            print(
                "      Status: ONLINE"
            )

        else:

            print(
                "      ⚠️ Internet connection unavailable."
            )

            print(
                "      Status: OFFLINE"
            )

    except Exception as error:

        print(
            f"      NOVA INTERNET ERROR: {error}"
        )


# ============================================================
# WEBSITE
# ============================================================

def load_website():

    print(
        "[5/6] Loading Website..."
    )


# ============================================================
# SERVER
# ============================================================

def load_server():

    print(
        "[6/6] Starting Server..."
    )

    try:

        app = create_server()

        # ----------------------------------------------------
        # FLASK SERVER
        # ----------------------------------------------------

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

        print(
            "      Flask server started."
        )

        # ----------------------------------------------------
        # SYSTEM TRAY
        # ----------------------------------------------------

        tray_thread = threading.Thread(
            target=tray.start,
            daemon=True
        )

        tray_thread.start()

        print(
            "      System tray started."
        )

        # ----------------------------------------------------
        # WINDOW STATUS
        # ----------------------------------------------------

        def mark_online():

            time.sleep(0.5)

            try:

                window.update_status(
                    "Online"
                )

            except Exception as error:

                print(
                    f"NOVA WINDOW ERROR: {error}"
                )

        threading.Thread(
            target=mark_online,
            daemon=True
        ).start()

    except Exception as error:

        print(
            f"NOVA SERVER ERROR: {error}"
        )


# ============================================================
# REGISTER FUNCTIONS
# ============================================================

register_function(
    1,
    "Settings",
    load_settings
)

register_function(
    2,
    "Memory",
    load_memory
)

register_function(
    3,
    "Brain",
    load_brain
)

register_function(
    4,
    "Internet",
    load_internet
)

register_function(
    5,
    "Website",
    load_website
)

register_function(
    6,
    "Server",
    load_server
)


# ============================================================
# START NOVA
# ============================================================

def start_nova():

    print()

    print(
        "=" * 50
    )

    print(
        "           NOVA AI"
    )

    print(
        "=" * 50
    )

    print(
        "NOVA: Starting..."
    )

    print()

    # ========================================================
    # STARTUP
    # ========================================================

    load_settings()

    load_memory()

    load_brain()

    load_internet()

    load_website()

    load_server()

    # ========================================================
    # STARTUP COMPLETE
    # ========================================================

    print()

    print(
        "========================================"
    )

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
        "========================================"
    )

    print()

    print(
        "NOVA startup controls:"
    )

    print(
        "r  = restart one selected function"
    )

    print(
        "ra = restart entire startup"
    )

    print()

    # ========================================================
    # COMMAND LISTENER
    # ========================================================

    command_thread = threading.Thread(
        target=startup_command_listener,
        daemon=True
    )

    command_thread.start()

    # ========================================================
    # NOVA WINDOW
    # ========================================================

    window.start(
        start_hidden=True
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    start_nova()