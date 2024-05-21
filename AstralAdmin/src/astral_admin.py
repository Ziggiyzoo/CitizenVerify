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

        embed = discord.Embed(
            title="Welcome to Astral Admin",
            description=f"Greetings {member.mention}, and welcome to the Astral Dynamics Discord.",
            color=discord.Colour.blue()
        )
        embed.add_field(name="APPLY NOW",
                        value="To **Apply** to Astral Dynamics & gain access to the Discord Server," +
                         " click [**here**](https://robertsspaceindustries.com/orgs/ASTDYN/)")
        embed.add_field(name="REGISTER WITH OUR ADMIN ASSISTANT",
                        value=f"Please make your way to {welcome.mention} and utilise the" +
                         " `/bind-rsi-account` command until you have completed the process.")
        embed.add_field(name="Organisation Overview",
                        value="\n*Astral Dynamics focuses on providing* ***Resource Acquisition***,"
                         " ***Processing & Delivery*** *in a* ***Secure*** *and* ***Timely*** *Manner*.",
                        inline=False)
        await welcome.send(embed=embed)
