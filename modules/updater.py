import os
import re
import subprocess
import tempfile

import requests

import config
from modules.version import __version__


def _version(value):
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", value or "")
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


def get_latest_release():
    response = requests.get(
        config.UPDATE_CHECK_URL,
        headers={"Accept": "application/vnd.github+json"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def check_for_update():
    release = get_latest_release()
    latest = _version(release.get("tag_name", ""))
    current = _version(__version__)
    if latest <= current:
        return None

    msi_name = None
    msi_url = None
    for asset in release.get("assets", []):
        name = asset.get("name", "")
        if name.lower().endswith("-x64.msi"):
            msi_name = name
            msi_url = asset.get("browser_download_url")
            break

    if not msi_url:
        raise RuntimeError("The latest NOVA release does not contain an x64 MSI.")

    return {
        "version": ".".join(map(str, latest)),
        "tag": release.get("tag_name"),
        "name": msi_name,
        "url": msi_url,
        "release_url": release.get("html_url"),
    }


def install_update(update):
    """Download the latest MSI to a temporary file and launch Windows Installer."""
    fd, path = tempfile.mkstemp(prefix="NOVA-update-", suffix=".msi")
    os.close(fd)
    try:
        with requests.get(update["url"], stream=True, timeout=(20, 120)) as response:
            response.raise_for_status()
            with open(path, "wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)

        subprocess.Popen(["msiexec.exe", "/i", path, "/passive"], close_fds=True)
        return True
    except Exception:
        try:
            os.remove(path)
        except OSError:
            pass
        raise
