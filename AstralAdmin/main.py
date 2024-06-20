"""
Org Discord Bot
"""
import logging

from os import environ

from src.astral_admin import AstralAdmin

logger = logging.getLogger(__name__)

# Get Logging Level
if "DEPLOYMENT_ENV" not in environ or environ["DEPLOYMENT_ENV"] == "":
    log_level = 10
    log_file = "astralAdmin.log"
elif environ["DEPLOYMENT_ENV"] == "DEV":
    log_level = 20
    log_file = environ["/mnt/logs"]
else:
    log_level= 30
    log_file = environ["/mnt/logs"]

logging.basicConfig(filename=log_file, level=log_level,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(lineno)d:%(message)s")

# Main Method
if __name__ == "__main__":
    try:
        logger.info("Getting Token")
        token: str = environ["TOKEN"]
        test_api_key: str = environ["SC_API_KEY"]
        test_firebase_secret: str = environ["FIREBASE_SECRET"]
        Bot: AstralAdmin = AstralAdmin()
        Bot.load_extensions("src.cogs", recursive=True)
        Bot.run(token)
    except KeyError as exc:
        logger.critical(f"Environment Variable {exc} does not exist. Exiting")
          