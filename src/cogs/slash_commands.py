import discord
import json
from discord.ext import commands

class SlashCommands(commands.Cog):
  """
  Helldivers Update Bot Slash Cogs
  """

  def __init__(self, bot):
    self.bot: commands.Bot = bot

  @commands.slash_command(
    name="ping", description="Ping! :)"
  )
  async def ping(self, ctx):
    """
    Ping! :)
    """
    await ctx.respond("Pong!")

def setup(bot):
  """
  Add cog to bot
  """
  bot.add_cog(SlashCommands(bot))