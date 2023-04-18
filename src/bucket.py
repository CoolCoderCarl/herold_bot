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

client = session.client(
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

    def check_dir(directory: str) -> bool:
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
    response = client.list_objects(Bucket=BUCKET_NAME)
    result = []
    for obj in response["Contents"]:
        result.append(obj["Key"])

    f_c = filter_conf(search_dir)
    result = filter(f_c, result)

    return random.choices(list(result)[1:])[0].split("/")[1]


def download_file_from_bucket(remote_directory: str, local_directory: Path) -> str:
    """
    Download random file from bucket
    :param remote_directory:
    :param local_directory:
    :return:
    """
    try:
        random_file = get_random_object(remote_directory)
        client.download_file(BUCKET_NAME, random_file, local_directory)
        logging.info(f"File {random_file} downloaded to f{local_directory}")
        logging.info(f"Directory {local_directory} - {os.listdir(local_directory)}")
        return random_file
    except Exception as err:
        logging.error(f"File not downloaded ! - {err}")
        return None


def prune_directory(directory_to_prune: Path):
    """
    Need to prune directory after downloading to evade container enlargement
    :param directory_to_prune:
    :return:
    """
    try:
        for file in os.listdir(directory_to_prune):
            os.remove(os.path.join(directory_to_prune, file))
        logging.info(f"Directory {directory_to_prune} was pruned !")
    except FileNotFoundError as dir_not_found:
        logging.error(
            f"Directory {directory_to_prune} was not pruned - {dir_not_found}"
        )
    except Exception as err:
        logging.error(f"Directory {directory_to_prune} was not pruned - {err}")


if __name__ == "__main__":
    pass
