import platform
import subprocess
import webbrowser

SYSTEM = platform.system()

# Common app name -> how to launch it per OS
APP_MAP = {
    "notepad": {"Windows": ["notepad"], "Darwin": ["open", "-a", "TextEdit"], "Linux": ["gedit"]},
    "calculator": {"Windows": ["calc"], "Darwin": ["open", "-a", "Calculator"], "Linux": ["gnome-calculator"]},
    "calc": {"Windows": ["calc"], "Darwin": ["open", "-a", "Calculator"], "Linux": ["gnome-calculator"]},
    "chrome": {"Windows": ["chrome"], "Darwin": ["open", "-a", "Google Chrome"], "Linux": ["google-chrome"]},
    "browser": {"Windows": ["chrome"], "Darwin": ["open", "-a", "Safari"], "Linux": ["xdg-open", "http://google.com"]},
    "explorer": {"Windows": ["explorer"], "Darwin": ["open", "."], "Linux": ["xdg-open", "."]},
    "files": {"Windows": ["explorer"], "Darwin": ["open", "."], "Linux": ["xdg-open", "."]},
    "word": {"Windows": ["winword"], "Darwin": ["open", "-a", "Microsoft Word"], "Linux": ["libreoffice", "--writer"]},
    "vscode": {"Windows": ["code"], "Darwin": ["open", "-a", "Visual Studio Code"], "Linux": ["code"]},
    "code": {"Windows": ["code"], "Darwin": ["open", "-a", "Visual Studio Code"], "Linux": ["code"]},
    "spotify": {"Windows": ["spotify"], "Darwin": ["open", "-a", "Spotify"], "Linux": ["spotify"]},
}


def open_app(app_name):
    """Try to open a known application. Returns True on success, False if unknown/failed."""
    app_name = app_name.lower().strip()
    entry = APP_MAP.get(app_name)

    if not entry:
        return False

    command = entry.get(SYSTEM)
    if not command:
        return False

    try:
        subprocess.Popen(command)
        return True
    except (OSError, FileNotFoundError):
        return False


def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")


def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
