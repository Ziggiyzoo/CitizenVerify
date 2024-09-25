"""
Astral Admin Cogs
"""

from src.cogs import background_tasks, slash_commands


def setup(bot):
    """
    Run the setup functions for cogs
    """
    slash_commands.setup(bot)
    background_tasks.setup(bot)
