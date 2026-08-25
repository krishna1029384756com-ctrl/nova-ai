"""Internet connectivity helpers for NOVA."""
import requests


def check_internet():
    try:
        response = requests.get("https://www.google.com", timeout=5, headers={"User-Agent": "NOVA-AI/1.0"})
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_internet_status():
    return "ONLINE" if check_internet() else "OFFLINE"
