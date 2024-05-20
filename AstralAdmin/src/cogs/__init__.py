"""
Astral Admin Cogs
"""
from src.cogs import slash_commands, background_tasks

def setup(bot):
    """
    Run the setup functions for cogs
    """
    slash_commands.setup(bot)
    background_tasks.setup(bot)
    