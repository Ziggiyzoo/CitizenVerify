"""
Module to update a users discord roles.
"""
import traceback
import logging
import discord

logger = logging.getLogger("AA_Logger")

from src.logic import rsi_lookup, firebase_db_connection

RANK_LIST = [
                "Affiliate Programme",
                "Employees",
                "Team Leaders",
                "Managers",
                "Directors",
                "Board Members"
                ]
ORG_ROLES_LIST = [
        "CEO",
        "Executive",
        "Marketing",
        "Human Resources"
    ]

async def update_user_roles(user_list: list, bot: discord.bot, guild_id: str):
    """
    Update the discord members roles based on the RSI site.
    """
    logger.info("Get Guild Members")
    guild = await bot.fetch_guild(int(guild_id))
    # Get List of Org Members
    org_membership_dict = await rsi_lookup.get_org_membership_info(
        spectrum_id=await firebase_db_connection.get_guild_sid(guild_id)
        )
    org_membership_list = org_membership_dict["data"]
    try:
        logger.info("Update User Roles")
        # Update Users in the Discord
        for user in user_list:
            if user is not None:
                user_handle = user["user_rsi_handle"]
                user = await guild.fetch_member(int(user["user_id"]))
                # Get Users Roles
                roles = [role.name for role in user.roles]
                if any(d["handle"] == user_handle for d in org_membership_list):
                    try:
                        user_membership_info = next((member for member in org_membership_list if member["handle"] == user_handle),
                                                    None)
                        if user_membership_info is None:
                            raise ValueError(
                                "User Membership Info Dictionary does not exist."
                            )
                    except ValueError as exc:
                        logger.error("%s for User %s", exc, user_handle)

                    # Check if the user already has membership role
                    if user_membership_info["stars"] == 0:
                        membership = "Astral Dynamics Affiliate"
                        remove_membership = "Astral Dynamics Member"
                    else:
                        membership = "Astral Dynamics Member"
                        remove_membership = "Astral Dynamics Affiliate"

                    if membership not in roles:
                        # Assign the role to the user
                        await user.add_roles(
                            *[
                                discord.utils.get(
                                    guild.roles,
                                    name=membership
                                )
                            ]
                        )
                        await user.remove_roles(
                            *[
                                discord.utils.get(
                                    guild.roles,
                                    name=remove_membership
                                )
                            ]
                        )
                    else:
                        # User already has this role
                        logger.debug("User %s already has this role", user_handle)

                    # Get users Rank
                    rank = RANK_LIST[user_membership_info["stars"]]
                    if rank not in roles:
                        # Assign the role to the user
                        await user.add_roles(
                            *[
                                discord.utils.get(
                                    guild.roles,
                                    name=rank
                                )
                            ]
                        )

                        for i in [1, 2, 3, 4, 5]:
                            await user.remove_roles(
                                discord.utils.get(
                                    guild.roles,
                                    name=RANK_LIST[user_membership_info["stars"] - i]
                                )
                            )
                    else:
                        # User already has this role
                        logger.debug("User %s already has this role", user_handle)

                    # Get User Organisation Role
                    org_roles = user_membership_info["roles"]
                    if org_roles != []:
                        # Add Org Roles they have
                        for org_role in org_roles:
                            if org_role not in roles:
                                await user.add_roles(
                                    discord.utils.get(
                                        guild.roles,
                                        name=org_role
                                    )
                                )
                        # Remove Org Roles they don't have
                        for org_role in ORG_ROLES_LIST:
                            if org_role not in org_roles:
                                await user.remove_roles(
                                    discord.utils.get(
                                        guild.roles,
                                        name=org_role
                                    )
                                )

                    else:
                        # User has no org roles
                        for org_role in ORG_ROLES_LIST:
                            if org_role in roles:
                                await user.remove_roles(
                                    discord.utils.get(
                                        guild.roles,
                                        name=org_role
                                    )
                                )

                else:
                    # User not in org
                    for org_role in ORG_ROLES_LIST:
                        if org_role in roles:
                            await user.remove_roles(
                                discord.utils.get(
                                    guild.roles,
                                    name=org_role
                                )
                            )
                    for rank_role in RANK_LIST:
                        if rank_role in roles:
                            await user.remove_roles(
                                discord.utils.get(
                                    guild.roles,
                                    name=rank_role
                                )
                            )
                    for membership_role in ["Astral Dynamics Affiliate", "Astral Dynamics Member"]:
                        if membership_role in roles:
                            await user.remove_roles(
                                discord.utils.get(
                                    guild.roles,
                                    name=membership_role
                                )
                            )
            else:
                raise AttributeError("User List returned None from the DB")
        return "Roles Updated"

    except AttributeError:
        # Uh Oh
        logger.error("Attribute Error while updating roles for %s: %s", user_handle, {traceback.format_exc()})
        return f"Failed to update role for User: {user_handle}. Error: {traceback.format_exc()}"

    except discord.DiscordException:
        # Uh Oh
        logger.error("Attribute Error while updating roles for %s: %s", user_handle, {traceback.format_exc()})
        return f"Failed to update role for User: {user_handle}. Error: {traceback.format_exc()}"
            