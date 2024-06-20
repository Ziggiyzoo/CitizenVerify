"""
Org Discord Bot
"""
import logging
from logging import handlers

from os import environ
import os

from src.astral_admin import AstralAdmin

logger = logging.getLogger("AA_Logger")
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)d:%(message)s")

# Check if the logging file exists
print(os.path.isdir("./logging/"))

# Get Logging Level
if "DEPLOYMENT_ENV" not in environ or environ["DEPLOYMENT_ENV"] == "":
    LOG_LEVEL = 10
elif environ["DEPLOYMENT_ENV"] == "DEV":
    LOG_LEVEL = 20
else:
    LOG_LEVEL= 30

log_handler = handlers.RotatingFileHandler("./logs/astralAdmin.log", maxBytes=16384, backupCount=10)
log_handler.setFormatter(log_formatter)
logger.setLevel(LOG_LEVEL)
log_handler.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

# Main Method
if __name__ == "__main__":
    try:
        logger.info("Getting Token")
        token: str = environ["TOKEN"]
        test_api_key: str = environ["SC_API_KEY"]
        test_firebase_secret: str = environ["FIREBASE_SECRET"]
        Bot: AstralAdmin = AstralAdmin()
        logger.debug("Load Extensions and Run Bot")
        Bot.load_extensions("src.cogs", recursive=True)
        Bot.run(token)
    except KeyError as exc:
        logger.critical("Environment Variable %s does not exist. Exiting", exc)
          