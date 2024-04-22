"""
Astral Admin Bot
"""
import logging
import discord
import discord.ext.commands as ext_commands

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

  async def on_message(self, message):
    """
    Bot On Message
    """
    # This bot currently does nothing on message!