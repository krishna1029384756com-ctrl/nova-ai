import os
import platform
import subprocess
import webbrowser
from urllib.parse import quote_plus


# ============================================================
# SYSTEM
# ============================================================

SYSTEM = platform.system()


# ============================================================
# APPLICATION MAP
# ============================================================

APP_MAP = {

    # --------------------------------------------------------
    # Windows / macOS / Linux
    # --------------------------------------------------------

    "notepad": {
        "Windows": ["notepad.exe"],
        "Darwin": ["open", "-a", "TextEdit"],
        "Linux": ["gedit"],
    },

    "calculator": {
        "Windows": ["calc.exe"],
        "Darwin": ["open", "-a", "Calculator"],
        "Linux": ["gnome-calculator"],
    },

    "calc": {
        "Windows": ["calc.exe"],
        "Darwin": ["open", "-a", "Calculator"],
        "Linux": ["gnome-calculator"],
    },

    "chrome": {
        "Windows": ["chrome.exe"],
        "Darwin": ["open", "-a", "Google Chrome"],
        "Linux": ["google-chrome"],
    },

    "browser": {
        "Windows": ["chrome.exe"],
        "Darwin": ["open", "-a", "Safari"],
        "Linux": ["xdg-open", "https://google.com"],
    },

    "explorer": {
        "Windows": ["explorer.exe"],
        "Darwin": ["open", "."],
        "Linux": ["xdg-open", "."],
    },

    "files": {
        "Windows": ["explorer.exe"],
        "Darwin": ["open", "."],
        "Linux": ["xdg-open", "."],
    },

    "word": {
        "Windows": ["winword.exe"],
        "Darwin": ["open", "-a", "Microsoft Word"],
        "Linux": ["libreoffice", "--writer"],
    },

    "vscode": {
        "Windows": ["code.cmd"],
        "Darwin": ["open", "-a", "Visual Studio Code"],
        "Linux": ["code"],
    },

    "code": {
        "Windows": ["code.cmd"],
        "Darwin": ["open", "-a", "Visual Studio Code"],
        "Linux": ["code"],
    },

    "spotify": {
        "Windows": ["spotify.exe"],
        "Darwin": ["open", "-a", "Spotify"],
        "Linux": ["spotify"],
    },

    # --------------------------------------------------------
    # GitHub Desktop
    # --------------------------------------------------------

    "github desktop": {
        "Windows": [
            os.path.expandvars(
                r"%LOCALAPPDATA%\GitHubDesktop\GitHubDesktop.exe"
            )
        ],
        "Darwin": [
            "open",
            "-a",
            "GitHub Desktop",
        ],
        "Linux": [
            "github-desktop"
        ],
    },

    "githubdesktop": {
        "Windows": [
            os.path.expandvars(
                r"%LOCALAPPDATA%\GitHubDesktop\GitHubDesktop.exe"
            )
        ],
        "Darwin": [
            "open",
            "-a",
            "GitHub Desktop",
        ],
        "Linux": [
            "github-desktop"
        ],
    },
}


# ============================================================
# HELPER
# ============================================================

def _expand_command(command):
    """
    Expand Windows environment variables and return
    a clean command list.
    """

    return [
        os.path.expandvars(str(part))
        for part in command
    ]


# ============================================================
# OPEN APPLICATION
# ============================================================

def open_app(app_name):
    """
    Try to open a known application.

    Returns:
        True  -> application launched
        False -> application unknown or failed
    """

    if not isinstance(app_name, str):
        return False

    app_name = app_name.strip().lower()

    if not app_name:
        return False

    entry = APP_MAP.get(app_name)

    if not entry:
        return False

    command = entry.get(SYSTEM)

    if not command:
        return False

    command = _expand_command(command)

    # --------------------------------------------------------
    # Windows path-based applications
    # --------------------------------------------------------

    if SYSTEM == "Windows":
        executable = command[0]

        # If this is an explicit file path, verify it exists.
        if (
            os.path.isabs(executable)
            and not os.path.isfile(executable)
        ):
            return False

    try:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
                if SYSTEM == "Windows"
                else 0
            ),
        )

        return True

    except (OSError, FileNotFoundError):
        return False


# ============================================================
# SEARCH WEB
# ============================================================

def search_web(query):
    """
    Open a Google search in the default browser.
    """

    if not isinstance(query, str):
        return False

    query = query.strip()

    if not query:
        return False

    url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    try:
        return webbrowser.open(url)

    except Exception:
        return False


# ============================================================
# OPEN WEBSITE
# ============================================================

def open_website(url):
    """
    Open a website in the default browser.
    """

    if not isinstance(url, str):
        return False

    url = url.strip()

    if not url:
        return False

    # --------------------------------------------------------
    # Add HTTPS if the user didn't provide a protocol.
    # --------------------------------------------------------

    if not url.startswith(
        (
            "http://",
            "https://",
        )
    ):
        url = "https://" + url

    try:
        return webbrowser.open(url)

    except Exception:
        return False


# ============================================================
# CHECK IF APP EXISTS
# ============================================================

def app_exists(app_name):
    """
    Check whether a registered application appears
    available on this system.
    """

    if not isinstance(app_name, str):
        return False

    app_name = app_name.strip().lower()

    entry = APP_MAP.get(app_name)

    if not entry:
        return False

    command = entry.get(SYSTEM)

    if not command:
        return False

    command = _expand_command(command)

    executable = command[0]

    # Absolute path
    if os.path.isabs(executable):
        return os.path.isfile(executable)

    # Search PATH
    try:
        import shutil

        return shutil.which(executable) is not None

    except Exception:
        return False


# ============================================================
# AVAILABLE APPLICATIONS
# ============================================================

def list_apps():
    """
    Return all registered application names.
    """

    return sorted(APP_MAP.keys())