import os
import boto3
import botocore
import random
from typing import List

import dynaconfig

session = boto3.session.Session()

BUCKET_NAME = dynaconfig.settings["BUCKET_NAME"]
ENDPOINT_URL = dynaconfig.settings["ENDPOINT_URL"]
REGION_NAME = dynaconfig.settings["REGION_NAME"]
AWS_ACCESS_KEY_ID = dynaconfig.settings["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = dynaconfig.settings["AWS_SECRET_ACCESS_KEY"]

CLIENT = session.client('s3',
                        endpoint_url=ENDPOINT_URL,
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name=REGION_NAME,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
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
    for obj in response['Contents']:
        result.append(obj['Key'])

    f_c = filter_conf(search_dir)
    result = filter(f_c, result)

    return random.choices(list(result)[1:])[0]


# CLIENT.download_file(BUCKET_NAME,
#                      'birthdays/birthdays-1.jpg',
#                      './')


if __name__ == '__main__':
    # print(os.listdir("birthdays"))

    print(get_random_object("birthdays"))
