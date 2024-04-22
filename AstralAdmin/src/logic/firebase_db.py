"""
Astral Admin database connection.
"""
import datetime
import os

import firebase_admin
from firebase_admin import credentials, firestore, exceptions

from os import environ

# from src.logic import _get_firebase_secret_path


def _get_firebase_secret_path() -> str:
    if os.name == "nt":
        return f"F:/Repos/AstralAdmin/AstralAdmin/src/logic/firebase_secrets.json"
    else:
        return "/var/secrets/firebase_secret.json"

cred: credentials.Certificate = credentials.Certificate(_get_firebase_secret_path())

firebase_admin.initialize_app(cred)
db = firestore.client()

users_col = db.collection("users")

async def new_user(author_id: int, guild_id: int, user_verification_code: str, rsi_handle: str):
    """
    Add New user to the DB
    """
    user_ref = users_col.document(f"{author_id}")
    try:
        # Set the User Fields
        user_ref.set(
            {
                "user_id": str(author_id),
                "user_verification_code": user_verification_code,
                "user_verification_progress": 0,
                "user_verification_status": False,
                "user_rsi_handle": rsi_handle
            }
        )

        # Create & set the fields of the Users Guilds Collection
        user_ref.collection("user_guilds").document(str(guild_id)).set(
            {
                "verified": False
            }
        )
        return True
    except exceptions.FirebaseError as exc:
        return False
