import logging

import sqlalchemy
from sqlalchemy import exc

import models

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def connect(db_name="herold_database.db"):
    return sqlalchemy.create_engine(f"sqlite:///{db_name}", echo=False).connect()


def create_db():
    try:
        models.META.create_all(connect())
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while creating db - {sql_err}")


def get_all_rows():
    """
    Query all rows from the db
    :return:
    """
    try:
        return connect().execute(models.PEOPLE.select()).fetchall()
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while fetching from {models.PEOPLE} db - {sql_err}")


def get_tg_id(current_date) -> str:
    for d in get_all_rows():
        if d[1] == current_date:
            return d[3]
    return None


if __name__ == "__main__":
    print(get_tg_id("05.11"))
    pass
