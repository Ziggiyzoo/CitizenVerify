"""
Astral Admin Bot
"""
import discord
import discord.ext.commands as ext_commands

# pylint: disable=too-many-ancestors
class AstralAdmin(ext_commands.Bot):
    """
    Helldivers Update Bot
    """

    def __init__(self):
        super().__init__(self, intents=discord.Intents.all())

    async def on_ready(self):
        """
        Bot On Ready
        """
        # This bot currently does nothing on ready
        info = self.get_channel(1233738280118390795)
        await info.send("Astral Dynamics Assistant is ready!")

    async def on_message(self, message):
        """
        Bot On Message
        """
        # This bot currently does nothing on message!

    async def on_member_join(self, member):
        """
        Send Message to New Member
        """
        welcome = self.get_channel(1230973934048903178)
        await welcome.send("Welcome to the Astral Dynamics Discord <@" + str(member.id)
                                   + ">. Please use the /bind-rsi-account so I may begin to"
                                   + " assist you through your application to Astral Dynamics.")
