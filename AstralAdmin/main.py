"""
Org Discord Bot
"""
import logging
import logging.handlers as handlers

from os import environ

from src.astral_admin import AstralAdmin

logger = logging.getLogger("AA_Logger")
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)d:%(message)s")

# Get Logging Level
if "DEPLOYMENT_ENV" not in environ or environ["DEPLOYMENT_ENV"] == "":
    log_level = 10
    log_file = "./logs/astralAdmin.log"
elif environ["DEPLOYMENT_ENV"] == "DEV":
    log_level = 20
    log_file = environ["/mnt/logs/astralAdmin.log"]
else:
    log_level= 30
    log_file = environ["/mnt/logs/astralAdmin.log"]

log_handler = handlers.RotatingFileHandler(log_file, maxBytes=16384, backupCount=10)
log_handler.setFormatter(log_formatter)
logger.setLevel(log_level)
log_handler.setLevel(log_level)
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
        logger.critical(f"Environment Variable {exc} does not exist. Exiting")
          