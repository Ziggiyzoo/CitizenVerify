"""
All the logic for slash commands
"""
import random
import string
import logging
import discord

from src.logic import firebase_db_connection, rsi_lookup, update_user_roles

logger = logging.getLogger("AA_Logger")

class SlashCommandsLogic():

  def __init__(self):
    """
    Init
    """

  async def ping():
    """
    Ping?.. Pong!! The most basic of tests.
    """
    return "Pong"