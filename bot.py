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

answers = [
    """
Hello. This is an auto-generated answer just for you. \n 

You have been pseudorandomly selected to test a new bot. \n

Congratulations, it's absolutely free. \n

Soon I will come to you, but it's not certain. \n

GL HF
"""
]


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
            return user_ids
    except FileNotFoundError as file_not_found_err:
        logging.error(file_not_found_err)


@client.on(events.NewMessage)
async def handle_new_message(event):

    user_ids = load_user_ids_from_file()
    print(user_ids)

    try:
        from_user = await event.client.get_entity(event.from_id)
        print(from_user)
        # print(from_user.first_name)
        # print(type(from_user.id))

        if from_user.id in user_ids:
            logging.info(event.message)
            logging.info(event.message.message)
            await asyncio.sleep(random.randrange(3, 15))
            if random.choice([True, False]):
                i, s = random.randrange(2, 5), random.choice(answers)
                async with client.action(from_user.id, "typing"):
                    await asyncio.sleep(i)
                    await client.send_message(from_user.id, s)
                    logging.info("Message was sent.")
    except ValueError as val_err:
        logging.error(val_err)
    except TypeError as type_err:
        logging.error("That maybe sticker was sent, not text.")
        logging.error(type_err)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
