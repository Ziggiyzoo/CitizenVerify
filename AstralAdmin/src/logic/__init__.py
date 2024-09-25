"""
Logic for the Astral Admin bot
"""

import os


def _get_firebase_secret_path() -> str:
    if os.name == "nt":
        return f"{os.getenv('LOCALAPPDATA')}\\secrets\\firebase_secret.json"

    return "/var/secrets/firebase_secret.json"
