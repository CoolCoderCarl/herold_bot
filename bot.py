import codecs
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import List

from telethon import TelegramClient

import db

# Environment variables
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

CLIENT = TelegramClient(SESSION, API_ID, API_HASH)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def load_congrats_from_files(file: Path) -> List:
    """
    Load congrats from the file
    Try to load from file, if exception caught, send message about err
    :return:
    """
    try:
        with codecs.open(Path(file), "r", "utf-8") as file:
            result = file.readlines()
            logging.info(f"Uploaded response from the {file.name} done successfully.")
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(f"Err while load file - {file_not_found_err}")
        return None


CONGRATULATIONS_FILE = load_congrats_from_files(Path("congrats_file.txt"))


async def send_congratulations():
    """
    Send congratulations if date is correct
    Wait for one day to check date
    :return:
    """
    current_date = datetime.today().strftime("%m.%d")
    if db.get_tg_id(current_date) is None:
        logging.info(f"Today - {current_date} - are no one to congratulate")
        time.sleep(86400)
    else:
        user_data = await CLIENT.get_entity(db.get_tg_id(current_date))
        logging.info(
            f"Today - {current_date} - going to congratulate {user_data.first_name} - {user_data.username}"
        )
        await CLIENT.send_message(
            db.get_tg_id(current_date), random.choice(CONGRATULATIONS_FILE)
        )
        time.sleep(86400)


async def main():
    while True:
        await send_congratulations()


if __name__ == "__main__":
    with CLIENT:
        CLIENT.loop.run_until_complete(main())
