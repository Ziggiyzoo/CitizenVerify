from src.cogs import slash_commands

def setup(bot):
  """
  Run the setup functions for cogs
  """
  slash_commands.setup(bot)