"""
Astral Admin RSI Lookup
"""

from os import environ
import httpx

import logging

logger = logging.getLogger("AA_Logger")

SC_API_KEY = environ["SC_API_KEY"]


async def get_org_membership_info(spectrum_id: str):
    """
    Return an Orgs Membership list
    """
    logger.info("Get Org Membership Info")
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/live/organization_members/{spectrum_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if str(response) != "<Response [200 OK]>":
            raise ConnectionError(str(response))
    except ConnectionError as exc:
        logger.error(f"Error getting Spectrum User: {exc}")
        return None


    return response.json()

async def get_user_info(rsi_handle: str):
    """
    Return a Users RSI Page info
    """
    logger.info("Get User Info")
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/eager/user/{rsi_handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if str(response) != "<Response [200 OK]>":
            raise ConnectionError(str(response))
    except ConnectionError as exc:
        logger.error(f"Error getting Spectrum User: {exc}")
        return None
    except httpx.ReadTimeout as exc:
        logger.error(f"Reading the Spectrum User page took too long: {exc}")
        return None

    return response.json()

async def verify_rsi_handle(rsi_handle, verification_code):
    """
    Get the info on the RSI Users About me.
    """
    logger.info("Get User About Me")
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/eager/user/{rsi_handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    except httpx.ReadTimeout as exc:
        logger.error(exc)
        return None
    contents = response.json()
    if contents["data"] is not None:
        try:
            if verification_code in contents["data"]["profile"]["bio"]:
                return True
        except KeyError as exc:
            logger.error(exc)
            return False
    return False
