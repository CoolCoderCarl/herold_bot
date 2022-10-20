import asyncio
import logging
import os
import random
from typing import List

from telethon import TelegramClient, events

API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION"]

client = TelegramClient(SESSION, API_ID, API_HASH)

IGNORED_FILE = "user_list.txt"

answer = """
Hello. This is an auto-generated answer just for you. \n
You have been pseudorandomly selected to test a new bot. \n
Congratulations, it's absolutely free ! \n
Soon I will come to you, but it's not certain. \n
GL HF
"""


# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def load_user_ids_from_file() -> List[int]:
    """
    Load user ids from file
    Try to load from file, if exception caught, send message about err
    Also convert to int to compare with id from Telegram
    :return:
    """
    try:
        with open(IGNORED_FILE, "r") as users_ids_file:
            user_ids = [int(u_ids) for u_ids in users_ids_file.read().split()]
            logging.info("Uploaded from the file done successfully.")
            return user_ids
    except FileNotFoundError as file_not_found_err:
        logging.error(file_not_found_err)


@client.on(events.NewMessage)
async def handle_new_message(event):
    user_ids = load_user_ids_from_file()
    logging.info(f"Users id uploaded: {user_ids}")
    try:
        user_data = await event.client.get_entity(event.from_id)
        # Show usernames by id
        logging.info(user_data)
        # logging.info(user_data.first_name)
        # print(type(from_user.id))

        if user_data.id in user_ids:
            logging.info(
                f"User with name {user_data.first_name} - with ID: {user_data.id} - send message: {event.message}"
            )
            logging.info(event.message.message)
            logging.info("Waiting for answer...")
            await asyncio.sleep(random.randrange(3, 15))
            async with client.action(user_data.id, "typing"):
                await asyncio.sleep(random.randrange(2, 5))
                await client.send_message(user_data.id, answer)
                logging.info("Message was sent.")
    except ValueError as val_err:
        logging.error(val_err)
    except TypeError as type_err:
        logging.error("That maybe sticker was sent, not text.")
        logging.error(type_err)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
