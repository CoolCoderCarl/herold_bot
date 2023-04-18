import asyncio
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import List

from telethon import TelegramClient

import bucket
import db

# Environment variables
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

client = TelegramClient(SESSION, API_ID, API_HASH)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def load_congrats_from_file(file: Path) -> List[str]:
    """
    Load congrats from the file
    Try to load from file, if exception caught, send message about err
    :return:
    """
    try:
        with open(Path(file), "r", encoding="utf-8") as file:
            result = file.readlines()
            logging.info(f"Uploaded response from the {file.name} done successfully.")
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(f"Err while load file - {file_not_found_err}")
        return None


CONGRATULATIONS = load_congrats_from_file(Path("congrats_list.txt"))


async def send_congratulations():
    """
    Check if someone has a birthday on this date then send congratulation
    Wait for one day to check date
    :return:
    """
    current_date = datetime.today().strftime("%m.%d")
    if db.get_tg_id(current_date) is None:
        logging.info(f"Today - {current_date} - are no one to congratulate")
        time.sleep(86400)
    else:
        user_data = await client.get_entity(db.get_tg_id(current_date))
        logging.info(
            f"Today - {current_date} - going to congratulate {user_data.first_name} - {user_data.username}"
        )
        await client.send_message(
            db.get_tg_id(current_date), random.choice(CONGRATULATIONS)
        )
        async with client.action(user_data.id, "typing"):
            await asyncio.sleep(random.randrange(2, 5))
            await client.send_file(
                db.get_tg_id(current_date),
                bucket.download_file_from_bucket(Path("/home/")),
            )
    time.sleep(400)
    bucket.prune_directory(Path("/home/"))
    time.sleep(86000)


async def main():
    while True:
        await send_congratulations()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
