import asyncio
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
DEBUG_ENABLED = os.environ["DEBUG_ENABLED"]

CLIENT = TelegramClient(SESSION, API_ID, API_HASH)

# Users files
FRIENDS_IDS_FILE = Path("friends_ids_list.txt")
FAMILIAR_IDS_FILE = Path("familiar_ids_list.txt")

# Response files
FRIENDS_RESPONSE_FILE = Path("friend_response.txt")
FAMILIAR_RESPONSE_FILE = Path("familiar_response.txt")
HR_RESPONSE_FILE = Path("hr_response.txt")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def load_ids_from_files(file: Path) -> List[int]:
    """
    Load user ids from the files
    Try to load from file, if exception caught, send message about err
    Also convert to int to compare with ids from Telegram
    :return:
    """
    try:
        with open(file, "r") as users_ids_file:
            result = [int(u_ids) for u_ids in users_ids_file.read().split()]
            if DEBUG_ENABLED:
                logging.debug("Uploaded ids from the file done successfully.")
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(file_not_found_err)


FRIENDS_IDS = load_ids_from_files(FRIENDS_IDS_FILE)
FAMILIAR_IDS = load_ids_from_files(FAMILIAR_IDS_FILE)


def load_responses_from_files(file: Path) -> str:
    """
    Load responses from the files
    Try to load from file, if exception caught, send message about err
    :return:
    """
    try:
        with open(file, "r") as response_file:
            result = response_file.read()
            if DEBUG_ENABLED:
                logging.debug("Uploaded response from the file done successfully.")
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(file_not_found_err)


FRIEND_RESPONSE = load_responses_from_files(FRIENDS_RESPONSE_FILE)
FAMILIAR_RESPONSE = load_responses_from_files(FAMILIAR_RESPONSE_FILE)
HR_RESPONSE = load_responses_from_files(HR_RESPONSE_FILE)


async def show_selected_users():
    async for dialog in CLIENT.iter_dialogs():
        if dialog.id in FRIENDS_IDS:
            logging.info(f"Selected friends username: {dialog.name}; ID: {dialog.id}")
        elif dialog.id in FAMILIAR_IDS:
            logging.info(f"Selected familiar username: {dialog.name}; ID: {dialog.id}")


@CLIENT.on(events.NewMessage)
async def handle_new_message(event):
    await show_selected_users()

    user_data = await event.client.get_entity(event.from_id)
    logging.info(f"Raw sender data: {user_data}")
    try:
        if not user_data.contact:
            logging.info(
                f"Contact: {user_data.contact} -"
                f"username: {user_data.first_name} - "
                f"has ID: {user_data.id} - "
                f"sent message: {event.message.message}"
            )
            # await CLIENT.send_message(user_data.id, HR_RESPONSE)
        elif user_data.id in FRIENDS_IDS:
            logging.info(
                f"Username: {user_data.first_name} - "
                f"has ID: {user_data.id} - "
                f"sent message: {event.message.message}"
            )
            if DEBUG_ENABLED:
                logging.debug("Waiting for response...")
            await asyncio.sleep(random.randrange(3, 15))
            async with CLIENT.action(user_data.id, "typing"):
                await asyncio.sleep(random.randrange(2, 5))
                await CLIENT.send_message(
                    user_data.id,
                    f"""
Hello, {user_data.first_name}. \n
**This message was sent automatically.** \n
""",
                )
                await CLIENT.send_message(user_data.id, FRIEND_RESPONSE)
                if DEBUG_ENABLED:
                    logging.debug(f"Response was sent to {user_data.first_name}.")
    except ValueError as val_err:
        logging.error(f"Sender is {user_data.first_name}")
        logging.error(val_err)
    except TypeError as type_err:
        logging.error("That maybe sticker was sent, not text.")
        logging.error(f"Sender is {user_data.first_name}")
        logging.error(type_err)


if __name__ == "__main__":
    CLIENT.start()
    CLIENT.run_until_disconnected()
