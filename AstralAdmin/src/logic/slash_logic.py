"""
All the logic for slash commands
"""

import logging

import discord
from src.logic import firebase_db_connection, rsi_lookup, update_user_roles

logger = logging.getLogger("AA_Logger")


class SlashCommandsLogic:
    """
    Logic for Slash Commands
    """

    def __init__(self):
        """
        Init
        """

    async def ping(self):
        """
        Ping?.. Pong!! The most basic of tests.
        """
        return "Pong"

    async def check_db_for_discord_user(self, user, author_id: int, rsi_handle: str, guild_id: int, bot: discord.ext.commands.Bot, code: str):
        """
        Checks the DB for the a entry with this Discord User.
        """
        # Get Discord User Info from DB
        user_info = await firebase_db_connection.get_user(author_id)

        # If the Discord User is not in the DB, check if the RSI Handle is
        if user_info is None:

            # Check if the RSI Handle is in the DB.
            if await firebase_db_connection.check_rsi_handle(rsi_handle, guild_id):

                # Handle the User trying to sign up with a previously added RSI Account.
                logger.warning("The Discord User is trying to bind with an already bound RSI Handle.")
                try:
                    await bot.get_channel(1269758666416979970).send(f"Discord User has tried to sign up with already bound RSI Handle {rsi_handle}.")
                    return 0
                except discord.errors.Forbidden as exc:
                    logger.warning("The Bot does not have permission to message in this channel: %s", exc)
                    return 0
            else:

                # Handle the User not existing!
                logger.debug("User does not exist")
                try:

                    # Attempt to add the user to the DB
                    await self.add_user_to_db(user, author_id, guild_id, code)
                    return 1
                except ConnectionError as exc:
                    logger.error(exc)
                    return 0

        else:
            logger.debug("User Exists")

            # Get the users verification code and return it to them.
            return user_info["user_verification_code"]

    async def add_user_to_db(self, user, author_id: int, guild_id: int, code):
        """
        Add the user to the DB
        """
        await firebase_db_connection.put_new_user(
            self,
            str(author_id),
            str(guild_id),
            rsi_handle=user["data"]["profile"]["handle"],
            display_name=user["data"]["profile"]["display"],
            user_verification_code=code,
        )

    async def check_db_for_rsi_user(self, rsi_handle):
        """
        Checks if this RSI Handle has been already registered with the Guild.
        """
        # Is the value None?
        if rsi_handle is None:
            return None

        # Does the User info exist?
        user = await rsi_lookup.get_user_info(rsi_handle=rsi_handle)
        if user is None:
            return None
        return user

    async def validate_user(self, user_db_info, author_name: str, author_id: int, guild_id: int, ctx, bot: discord.ext.commands.Bot):
        """
        Validate the User.
        """
        # Check that the user has a Validation code.
        if user_db_info["user_verification_code"] is None:
            logger.error("The User has a Validation State of 1, but no Validation Code.")
            return False

        # Verify that the Validation Code is on the RSI Website.
        if await rsi_lookup.verify_rsi_handle(rsi_handle=user_db_info["rsi_handle"], verification_code=user_db_info["user_verification_code"]):
            logger.info("The user %s is Validated.", author_name)

            # The user is Validated. Update the User DB and Guild DB
            await firebase_db_connection.update_user_verification_status(
                author_id=author_id, user_verification_progress=2, user_verification_status=True
            )
            await firebase_db_connection.update_user_guild_verification(author_id=author_id, guild_id=guild_id, guild_verification_status=True)

            # Update the users roles
            logger.info("Update the Roles for %s.", author_name)
            user_list = []
            user_list.append(user_db_info)
            try:
                await update_user_roles.update_user_roles(user_list=user_list, bot=bot, guild_id=guild_id)
                await ctx.author.edit(nick=user_db_info["user_display_name"])
                await ctx.author.add_role(discord.utils.get(ctx.guild.roles, name="Account Bound"))
            except discord.errors.Forbidden as exc:
                logger.warning("Bot does not have permissions to update user %s: %s", author_name, exc)
