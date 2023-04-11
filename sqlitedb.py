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
    sqlalchemy.Column('day_month', sqlalchemy.String),
    sqlalchemy.Column('year', sqlalchemy.String),
    sqlalchemy.Column('tg_id', sqlalchemy.String),
    sqlalchemy.Column('congrats_file_path', sqlalchemy.String),
)

# TODO Class & inheritance it


def engine(database_name="herold_database.db"):
    return sqlalchemy.create_engine(f'sqlite:///{database_name}', echo=False)


def connection():
    return engine().connect()


def create_db():
    try:
        META.create_all(engine())
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while creating db - {sql_err}")


def get_all():
    """
    Query all rows from the db
    :return:
    """
    try:
        return connection().execute(PEOPLE.select()).fetchall()
    except exc.SQLAlchemyError as sql_err:
        logging.error(f"Err while fetching from {PEOPLE} db - {sql_err}")


# For one type of subclass
def get_tg_id(current_date) -> str:
    for d in get_all():
        if d[1] == current_date:
            return d[3]
    return ""


if __name__ == "__main__":
    print(get_tg_id("05.11"))
    pass
