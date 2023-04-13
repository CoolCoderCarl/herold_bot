import asyncio
import codecs
import logging
import os
import random
from pathlib import Path
from typing import List

from telethon import TelegramClient, events

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


def load_responses_from_files(file: Path) -> str:
    """
    Load responses from the files
    Try to load from file, if exception caught, send message about err
    :return:
    """
    try:
        with codecs.open(file, "r", "utf-8") as response_file:
            result = response_file.read()
            logging.info(
                f"Uploaded response from the {response_file.name} done successfully."
            )
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(f"Err while load file - {file_not_found_err}")
        return None


async def send_message_template(user_data, event, start_range, end_range):
    logging.info(
        f"Contact: {user_data.contact} -"
        f"username: {user_data.first_name} - "
        f"ID: {user_data.id} - "
        f"sent message: {event.message.message}"
    )
    logging.info("Waiting for response...")
    async with CLIENT.action(user_data.id, "typing"):
        await asyncio.sleep(random.randrange(start_range, end_range))
        await CLIENT.send_message(
            user_data.id,
            f"""
Hello, {user_data.first_name}. \n
**This message was sent automatically.** \n
""",
        )
        await CLIENT.send_message(
            user_data.id,
        )
        logging.info(f"Response was sent to {user_data.first_name}.")


if __name__ == "__main__":
    CLIENT.start()
    CLIENT.run_until_disconnected()
