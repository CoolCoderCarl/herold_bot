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


def connect_to_db(db_name="herold_database.db") -> sqlalchemy.engine.base.Connection:
    return sqlalchemy.create_engine(f"sqlite:///{db_name}", echo=False).connect()


def create_db():
    try:
        models.meta.create_all(connect_to_db())
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while creating db - {sql_err}")


def get_all_people_from_db(model):
    """
    Query all rows from the db
    :return:
    """
    try:
        return connect_to_db().execute(model.birthdays.select()).fetchall()
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while fetching from {models.birthdays} db - {sql_err}")


def get_tg_id(current_date) -> str:
    """
    Get telegram ID if today is anyone to congrats
    :param current_date:
    :return:
    """
    for d in get_all_people_from_db(model=models):
        if current_date == d[1]:
            logging.info(f"{d[1]} = {current_date}")
            return d[3]
    return None


# TODO Add update db from file

if __name__ == "__main__":
    pass
