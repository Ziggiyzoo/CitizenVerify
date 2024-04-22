"""
Astral Admin RSI Lookup
"""

from os import environ
import httpx

SC_API_KEY = environ["SC_API_KEY"]

async def check_rsi_handle(rsi_handle):
    """
    Check if the given RSI handle is valid
    """
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/auto/user/{rsi_handle}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    contents = response.json()
    if str(response) == "<Response [200 OK]>" and contents["data"] is not None:
        return contents["data"]["profile"]["handle"]

    return None


async def verify_rsi_handle(rsi_handle, verification_code):
    """
    Get the info on the RSI Users About me.
    """
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/live/user/{rsi_handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    except httpx.ReadTimeout as error:
        return None
    contents = response.json()
    if contents["data"] is not None:
        if verification_code in contents["data"]["profile"]["bio"]:
            return True
    else:
        return False
    return False


async def get_user_membership_info(rsi_handle):
    """
    Check if the user is a member, and check if they are a affilliate or main member.
    """
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/auto/user/{rsi_handle}"
    membership = {"main_member": None, "member_rank": None}
    skip = False
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if str(response) != "<Response [200 OK]>":
        skip = True

    if not skip:
        contents = response.json()
        # Check if BRVNS is the main ORG
        try:
            if contents["data"]["organization"]["name"] == "Blue Ravens Inc":
                membership["main_member"] = True
                membership["member_rank"] = contents["data"]["organization"]["stars"]
            else:
                membership["main_member"] = False
                membership["member_rank"] = contents["data"]["organization"]["stars"]
        except TypeError as error:
            return None

    return membership