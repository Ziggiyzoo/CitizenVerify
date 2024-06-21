"""
Org Discord Bot
"""
import logging
import sys

from logging import StreamHandler

from os import environ

from src.astral_admin import AstralAdmin

logger = logging.getLogger("AA_Logger")
log_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)d:%(message)s")
log_handler = StreamHandler(sys.stderr)
log_handler.setFormatter(log_formatter)

# Get Logging Level
if "DEPLOYMENT_ENV" not in environ or environ["DEPLOYMENT_ENV"] == "":
    LOG_LEVEL = "DUBUG"
elif environ["DEPLOYMENT_ENV"] == "DEV":
    LOG_LEVEL = "INFO"
else:
    LOG_LEVEL = "WARNING"

logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

# Logging Test
print("Logging Test")
print(f"{environ["DEPLOYMENT_ENV"]}")
print(f"{LOG_LEVEL}")
logger.debug("DEBUG")
logger.info("INFO")
logger.warning("WARNING")
logger.error("ERROR")
logger.critical("CRITICAL")

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
          