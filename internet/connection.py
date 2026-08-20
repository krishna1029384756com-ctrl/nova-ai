"""
NOVA AI
Internet Connection Module
"""

import requests


def check_internet():
    """
    Check whether NOVA has an active internet connection.

    Returns:
        bool: True if internet is available, otherwise False.
    """

    try:
        response = requests.get(
            "https://www.google.com",
            timeout=5,
            headers={
                "User-Agent": "NOVA-AI/1.0"
            }
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def get_internet_status():
    """
    Get NOVA's internet status as readable text.

    Returns:
        str: Internet status.
    """

    if check_internet():
        return "🟢 Online"

    return "🔴 Offline"