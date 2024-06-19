"""
Org Discord Bot
"""
import logging

from os import environ

from src.astral_admin import AstralAdmin

logging.basicConfig(filename="test.log", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s:%(pathname)s:%(lineno)d")

# Main Method
if __name__ == "__main__":
    try:
        logging.info("Getting Token")
        token: str = environ["TOKEN"]
        test_api_key: str = environ["SC_API_KEY"]
        test_firebase_secret: str = environ["FIREBASE_SECRET"]
        Bot: AstralAdmin = AstralAdmin()
        Bot.load_extensions("src.cogs", recursive=True)
        logging.info("Cogs Loaded, running bot.")
        Bot.run(token)
    except KeyError as exc:
        logging.critical(f"Environment Variable {exc} does not exist. Exiting.")
          