"""
Background Tasks to loop for the bot.
"""

import logging

from discord.ext import commands  # , tasks

# from src.logic import firebase_db_connection, update_user_roles

logger = logging.getLogger("AA_Logger")


class BackgroundTasks(commands.Cog):
    """
    Background Tasks
    """

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        logger.info("Start Update Org Roles Task")
        self.update_org_roles.start()

    # # pylint: disable=duplicate-code
    # @tasks.loop(hours=1)
    # async def update_org_roles(self):
    #     """
    #     Automatic trigger to update Discord roles based of the RSI Org page.
    #     """
    #     logger.info("Running Role Update Background Task")
    #     guild_ids = await firebase_db_connection.get_guild_ids()
    #     for guild_id in guild_ids:
    #         # Get list of verified members in the guild
    #         guild_members = await firebase_db_connection.get_guild_members(guild_id=guild_id)

    #         # Get verified member info
    #         user_list = []
    #         for member_id in guild_members:
    #             user_list.append(await firebase_db_connection.get_user(author_id=str(member_id)))

    #         response = await update_user_roles.update_user_roles(user_list=user_list, bot=self.bot, guild_id=guild_id)
    #         if response is not None:
    #             log_here = self.bot.get_channel(1233738280118390795)
    #             await log_here.send(response)


def setup(bot):
    """
    Add Cog to Bot
    """
    bot.add_cog(BackgroundTasks(bot))
    logger.info("Background Tasks Cog Added")
