"""
Astral Admin RSI Lookup
"""

from os import environ
import httpx

SC_API_KEY = environ["SC_API_KEY"]


async def get_org_membership_info(spectrum_id: str):
    """
    Return an Orgs Membership list
    """
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/live/organization_members/{spectrum_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if str(response) != "<Response [200 OK]>":
            raise ConnectionError(str(response))
    except ConnectionError as exc:
        print(exc)
        return None
    except httpx._exceptions as exc:
        print(exc)
        return None


    return response.json()

async def get_user_info(rsi_handle: str):
    """
    Return a Users RSI Page info
    """
    url = f"https://api.starcitizen-api.com/{SC_API_KEY}/v1/eager/user/{rsi_handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if str(response) != "<Response [200 OK]>":
            raise ConnectionError(str(response))
    except ConnectionError as exc:
        print(exc)
        return None
    except httpx.ReadTimeout as exc:
        print(exc)
        return None

    return response.json()
