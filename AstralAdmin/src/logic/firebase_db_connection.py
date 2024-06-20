"""
Astral Admin database connection.
"""
import json
from os import environ
import logging
import firebase_admin
from firebase_admin import credentials, firestore, exceptions

logger = logging.getLogger("AA_Logger")

cred: credentials.Certificate = credentials.Certificate(json.loads(environ["FIREBASE_SECRET"]))

firebase_admin.initialize_app(cred)
db = firestore.client()

users_col = db.collection("users")
guilds_col = db.collection("guilds")

async def put_new_user(author_id: str,
                       guild_id: str,
                       user_verification_code: str,
                       rsi_handle: str,
                       display_name: str):
    """
    Add New User to the DB
    """
    logger.info("Try to Put New User in the Firebase DB")
    user_ref = users_col.document(f"{author_id}")
    try:
        # Set the User Fields
        user_ref.set(
            {
                "user_id": str(author_id),
                "user_verification_code": f"{user_verification_code}",
                "user_verification_progress": 0,
                "user_verification_status": False,
                "user_rsi_handle": f"{rsi_handle}",
                "user_display_name": f"{display_name}"
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
        logger.error("Error putting new user into Firebase DB: %s", exc)
        return False

async def put_new_guild(guild_id: str,
                        guild_name: str,
                        spectrum_id:str):
    """
    Add New Guild to the DB
    """
    logger.info("Try and Put new Guild in the Firebase DB")
    guild_ref = guilds_col.document(f"{guild_id}")
    try:
        # Set the Guilds Fields
        guild_ref.set(
            {
                "guild_name": guild_name,
                "guild_spectrum_id": spectrum_id,
                "guild_id": guild_id
            }
        )
        return True
    except exceptions.FirebaseError as exc:
        logger.error("Error Putting New Guild in the Firebase DB: %s", exc)
        return False

async def del_guild(guild_id: str):
    """
    Delete Guild from the DB
    """
    logger.info("Try and delete Guild from Firebase DB")
    guild_ref = guilds_col.document(f"{guild_id}")
    try:
        guild_ref.delete()
        return True
    except exceptions.FirebaseError as exc:
        logger.error("Error Deleting Guild from Firebase DB: %s", exc)
        return False

async def update_user_verification_status(author_id: str,
                                          user_verification_progress: int,
                                          user_verification_status: bool):
    """
    Update User Doc with Verification info
    """
    logger.info("Try to Update User Verification Status")
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
        logger.error("Error Updating the User Varification Status in the Firebase DB: %s", exc)
        return False

# pylint: disable=no-member
async def update_user_guild_verification(author_id: str,
                                         guild_id: str,
                                         guild_verification_status: bool):
    """
    Update User Doc with time of  Guild Verification Info
    """
    logger.info("Try to Update User Guild Verification")
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
        logger.error("Error Update the Guild Verification Status: %s", exc)
        return False

async def get_user(author_id: str):
    """
    Get the User
    """
    logger.info("Try to Get The User from Database")
    try:
        user_ref = users_col.document(f"{author_id}")
    except exceptions.FirebaseError as exc:
        logger.error("Error getting user %s from the database: %s", author_id, exc)
        return None
    if user_ref.get().exists:
        return user_ref.get().to_dict()
    return None

async def get_user_guild(author_id: str,
                         guild_id: str):
    """
    Get the Users Guild Info
    """
    logger.info("Try to get the User's Guild from the DB")
    try:
        user_ref = users_col.document(f"{author_id}").collection("user_guilds").document(f"{guild_id}")
    except exceptions.FirebaseError as exc:
        logger.error("Error getting Users Guild from the Firebase DB: %s", exc)
        return None
    if user_ref.get().exists:
        return user_ref.get().to_dict()
    return None

async def get_guild_members(guild_id: str):
    """
    Get a list of verified Guild Members
    """
    logger.info("Try to get a List of Verified Guild Members from the DB")
    try:
        guild_member_info = guilds_col.document(f"{guild_id}").collection("members").select(field_paths=[]).get()
    except exceptions.FirebaseError as exc:
        logger.error("Error in Getting List of Guild Members from the Firebase DB: %s", exc)
        return None
    if guild_member_info is not None:
        guild_members = [member.id for member in guild_member_info]
        return guild_members
    return None

async def get_guild_ids():
    """
    Get a list of added guilds
    """
    logger.info("Try and get a List of Guilds from the DB")
    try:
        docs = guilds_col.stream()
    except exceptions.FirebaseError as exc:
        logger.error("Error in Getting List of Guilds from the Firebase DB: %s", exc)
        return None
    if docs is not None:
        guild_ids = [doc.to_dict()["guild_id"] for doc in docs]
        return guild_ids
    return None

async def get_guild_sid(guild_id: str):
    """
    Get Guild SID
    """
    logger.info("Try Getting Guild SID from the DB")
    try:
        return guilds_col.document(f"{guild_id}").get().to_dict()["guild_spectrum_id"]

    except exceptions.FirebaseError as exc:
        logger.error("Error in Getting Guild SID from the Firebase DB: %s", exc)
        return None

# async def del_user(guild_id: str, user_id: str):
#     """
#     When a member leaves a guild, delete the user reference from the Guild & User Collection
#     """
#     logger.info("Try and Delete user from all locations in the DB")

    # TO DO
        # Del from Users Collection
        # Del from Guild
