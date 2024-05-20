"""
Background Tasks to loop for the bot.
"""

from discord.ext import commands, tasks
from src.logic import firebase_db_connection, update_user_roles

class BackgroundTasks(commands.Cog):
    """
    Background Tasks
    """

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print("Init Background Tasks")
        self.update_org_roles.start()

    #  pylint: disable=no-member
    @tasks.loop(hours=1)
    async def update_org_roles(self):
        """
        Automatic trigger to update Discord roles based of the RSI Org page.
        """
        guild_ids = await firebase_db_connection.get_guild_ids()
        for guild_id in guild_ids:
            # Get list of verified members in the guild
            guild_members = await firebase_db_connection.get_guild_members(guild_id=guild_id)

            # Get verified member info
            user_list = []
            for member_id in guild_members:
                user_list.append(
                    await firebase_db_connection.get_user(author_id=str(member_id))
                )

            response = await update_user_roles.update_user_roles(user_list=user_list, bot=self.bot, guild_id=guild_id)
            if response is not None:
                log_here = self.bot.get_channel(1233738280118390795)
                await log_here.send(response)

def setup(bot):
    """
    Add Cog to Bot
    """
    bot.add_cog(BackgroundTasks(bot))
    print("Background Tasks Cog Added")
