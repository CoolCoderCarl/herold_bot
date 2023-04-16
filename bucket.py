import logging
import os
import random
from pathlib import Path

import boto3
import botocore

import dynaconfig

session = boto3.session.Session()

BUCKET_NAME = dynaconfig.settings["BUCKET_NAME"]
ENDPOINT_URL = dynaconfig.settings["ENDPOINT_URL"]
REGION_NAME = dynaconfig.settings["REGION_NAME"]
AWS_ACCESS_KEY_ID = dynaconfig.settings["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = dynaconfig.settings["AWS_SECRET_ACCESS_KEY"]

CLIENT = session.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    config=botocore.config.Config(s3={"addressing_style": "virtual"}),
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def filter_conf(dir_to_filter):
    """
    Configure what to filter from the list files of directory
    :param dir_to_filter:
    :return:
    """

    def check_dir(directory: str):
        """
        Check the needed directory
        :param directory:
        :return:
        """
        return True if directory.startswith(dir_to_filter) else False

    return check_dir


def get_random_object(search_dir: str) -> str:
    """
    Get random object from searched directory in bucket
    :param search_dir:
    :return:
    """
    response = CLIENT.list_objects(Bucket=BUCKET_NAME)
    result = []
    for obj in response["Contents"]:
        result.append(obj["Key"])

    f_c = filter_conf(search_dir)
    result = filter(f_c, result)

    return random.choices(list(result)[1:])[0].split("/")[1]


def download_file_from_bucket(target_dir: Path):
    # random_file = ""
    try:
        random_file = get_random_object("birthdays")
        CLIENT.download_file(BUCKET_NAME, random_file, target_dir)
        logging.info(f"File {random_file} downloaded to f{target_dir}")
        logging.info(f"Directory {target_dir} - {os.listdir(target_dir)}")
        return random_file
    except Exception as err:
        logging.error(f"File not downloaded ! - {err}")


if __name__ == "__main__":
    pass
