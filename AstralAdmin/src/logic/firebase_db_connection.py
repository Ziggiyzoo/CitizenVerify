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
guilds_col = db.collection("guilds")

async def put_new_user(author_id: int, guild_id: int, user_verification_code: str, rsi_handle: str):
    """
    Add New User to the DB
    """
    user_ref = users_col.document(f"{author_id}")
    try:
        # Set the User Fields
        user_ref.set(
            {
                "user_id": str(author_id),
                "user_verification_code": f"{user_verification_code}",
                "user_verification_progress": 0,
                "user_verification_status": False,
                "user_rsi_handle": f"{rsi_handle}"
            }
        )

        # Create & set the fields of the Users Guilds Collection
        user_ref.collection("user_guilds").document(str(guild_id)).set(
            {
                "verified": False,
                "verified_on": None
            }
        )
        return True
    except exceptions.FirebaseError as exc:
        return False

async def put_new_guild(guild_id: int, guild_name: str, spectrum_id:str):
    """
    Add New Guild to the DB
    """
    guild_ref = guilds_col.document(f"{guild_id}")
    try:
        # Set the Guilds Fields
        guild_ref.set(
            {
                "guild_name": guild_name,
                "guild_spectrum_id": spectrum_id
            }
        )
        return True
    except exceptions.FirebaseError as exc:
        return False
    
async def del_guild(guild_id: int):
    """
    Delete Guild from the DB
    """
    guild_ref = guilds_col.document(f"{guild_id}")
    try:
        guild_ref.delete()
        return True
    except exceptions.FirebaseError as exc:
        return False

async def update_user_verification_status(author_id: str, user_verification_progress: int, user_verification_status: bool):
    """
    Update User Doc with Verification info
    """
    user_ref = users_col.document(f"{author_id}")
    try:
        # Update the User Fields
        user_ref.update(
            {
                "user_verification_progress": user_verification_progress,
                "user_verification_status": user_verification_status
            }
        )
        return True
    except exceptions.FirebaseError as exc:
        return False

async def update_user_guild_verification(author_id: str, guild_id: str, guild_verification_status: bool):
    """
    Update User Doc with Guild Verification Info
    """
    user_guild_ref = users_col.document(f"{author_id}").collection("user_guilds").document(f"{guild_id}")
    guild_ref = guilds_col.document(f"{guild_id}").collection("members").document(f"{author_id}")
    try:
        # Update User Guild Collection
        user_guild_ref.set(
            {
                "verified": guild_verification_status,
                "verified_on": firestore.SERVER_TIMESTAMP,
            }
        )

        # Set Guild User information
        guild_ref.set(
            {
                "verified": guild_verification_status,
                "verified_on": firestore.SERVER_TIMESTAMP,
                "user": author_id
            }
        )
        return True
    except exceptions.FirebaseError as exc:
        return False

async def get_user(author_id: str):
    """
    Get the User
    """
    try:
        user_ref = users_col.document(f"{author_id}")
    except exceptions.FirebaseError as exc:
        print(exc)
        return None
    
    if user_ref.get().exists:
        return user_ref.get().to_dict()
    else:
        return None
    
async def get_user_guild(author_id: str, guild_id: str):
    """
    Get the Users Guild Info
    """
    try:
        user_ref = users_col.document(f"{author_id}").collection("user_guilds").document(f"{guild_id}")
    except exceptions.FirebaseError as exc:
        return None
    
    if user_ref.get().exists:
        return user_ref.get().to_dict()
    else:
        return None

async def get_verified_guild_members(guild_id: int):
    """
    Get a list of verified Guild Members
    """