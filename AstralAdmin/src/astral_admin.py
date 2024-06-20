"""
Astral Admin Bot
"""
import logging
import discord
import discord.ext.commands as ext_commands


logger = logging.getLogger("AA_Logger")

# pylint: disable=too-many-ancestors
class AstralAdmin(ext_commands.Bot):
    """
    Astral Admin Assistant Bot
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
        logger.info("Astral Dynamics Assistant Bot is ready")

    async def on_message(self, message):
        """
        Bot On Message
        """
        # This bot currently does nothing on message!

    async def on_member_join(self, member):
        """
        Send Message to New Member
        """
        logger.info("Try to Send Message in Welcome Channel")
        try:
            welcome = self.get_channel(1230973934048903178)
            lobby = self.get_channel(1231045018471501844)

            await welcome.send(member.mention)
            embed = discord.Embed(
                title="Welcome to Astral Admin",
                description=f"Greetings {member.name}, and welcome to the Astral Dynamics Discord.",
                color=discord.Colour.blue()
            )
            embed.add_field(name="APPLY NOW",
                            value="To **Apply** to Astral Dynamics & gain access to the Discord Server," +
                            " click [**here**](https://robertsspaceindustries.com/orgs/ASTDYN/)")
            embed.add_field(name="REGISTER WITH OUR ADMIN ASSISTANT",
                            value=f"Please make your way to {lobby.mention} and utilise the" +
                            " `/bind-rsi-account` command until you have completed the process.")
            embed.add_field(name="Organisation Overview",
                            value="\n*Astral Dynamics focuses on providing* ***Resource Acquisition***,"
                            " ***Processing & Delivery*** *in a* ***Secure*** *and* ***Timely*** *Manner*.",
                            inline=False)
            await welcome.send(embed=embed)
        except TypeError as exc:
            logger.error("%s", exc)
        except discord.DiscordException as exc:
            logger.error("%s", exc)
