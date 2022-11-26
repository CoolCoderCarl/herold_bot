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

# Users ID file
CIRCULATION_IDS_FILE = Path("circulation_ids_list.txt")

# Response
CIRCULATION_RESPONSE_FILE = Path("circulation_response.txt")


# Logging
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
            logging.info(
                f"Uploaded ids from the {users_ids_file.name} done successfully."
            )
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(file_not_found_err)


CIRCULATION_IDS = load_ids_from_files(CIRCULATION_IDS_FILE)


def load_responses_from_files(file: Path) -> str:
    """
    Load responses from the files
    Try to load from file, if exception caught, send message about err
    :return:
    """
    try:
        with codecs.open(str(file), "r", "utf-8") as response_file:
            result = response_file.read()
            logging.info(
                f"Uploaded response from the {response_file.name} done successfully."
            )
            return result
    except FileNotFoundError as file_not_found_err:
        logging.error(file_not_found_err)


CIRCULATION_RESPONSE = load_responses_from_files(CIRCULATION_RESPONSE_FILE)


async def show_selected_users():
    async for dialog in CLIENT.iter_dialogs():
        if dialog.id in CIRCULATION_IDS:
            logging.info(f"Selected username: {dialog.name}; ID: {dialog.id}")


async def send_message_template(
    user_data, event, start_range, end_range, response_type
):
    logging.info(
        f"Contact: {user_data.contact} - "
        f"first name: {user_data.first_name} - "
        f"ID: {user_data.id} - "
        f"sent message: {event.message.message}"
    )


#     logging.info("Waiting for response...")
#     async with CLIENT.action(user_data.id, "typing"):
#         await asyncio.sleep(random.randrange(start_range, end_range))
#         await CLIENT.send_message(
#             user_data.id,
#             f"""
# Hello, {user_data.first_name}. \n
# **This message was sent automatically.** \n
# """,
#         )
#         await CLIENT.send_message(user_data.id, response_type)
#         logging.info(f"Response was sent to {user_data.first_name}.")


@CLIENT.on(events.NewMessage)
async def response_to_group(event):
    await show_selected_users()

    user_data = await event.client.get_entity(event.from_id)

    logging.info(f"Raw sender data: {user_data}")

    try:
        if user_data.id in CIRCULATION_IDS:
            await send_message_template(user_data, event, 5, 10, CIRCULATION_RESPONSE)
        elif not user_data.contact:
            logging.info("Looks like someone unfamiliar is on the line.")
            logging.info(
                f"Contact: {user_data.contact} - "
                f"first name: {user_data.first_name} - "
                f"ID: {user_data.id} - "
                f"sent message: {event.message.message}"
            )
    except ValueError as val_err:
        logging.error(f"Sender is {user_data.first_name}.")
        logging.error(val_err)
    except TypeError as type_err:
        logging.error("That maybe sticker was sent, not text.")
        logging.error(f"Sender is {user_data.first_name}.")
        logging.error(type_err)
    except BaseException as base_exception:
        logging.error(f"Sender is {user_data.first_name}.")
        logging.error(base_exception)


if __name__ == "__main__":
    CLIENT.start()
    CLIENT.run_until_disconnected()
