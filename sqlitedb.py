import logging
# import sqlite3
# from sqlite3 import Error
import sqlalchemy
from sqlalchemy import exc

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)

META = sqlalchemy.MetaData()
PEOPLE = sqlalchemy.Table(
    'people', META,
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('date', sqlalchemy.String),
    sqlalchemy.Column('tg_id', sqlalchemy.String),
    sqlalchemy.Column('congrats_file_path', sqlalchemy.String),
)


def engine(database_name="herold_database.db"):
    return sqlalchemy.create_engine(f'sqlite:///{database_name}', echo=False)


def connection():
    return engine().connect()


def create_db():
    try:
        META.create_all(engine())
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while creating db - {sql_err}")


def get_all_people():
    """
    Query all rows in the people db table
    :return:
    """
    try:
        return connection().execute(PEOPLE.select()).fetchall()
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while fetching from {PEOPLE} db - {sql_err}")


if __name__ == "__main__":
    # print(get_all_people())
    pass
