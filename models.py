import sqlalchemy

META = sqlalchemy.MetaData()
PEOPLE = sqlalchemy.Table(
    "people",
    META,
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("day_month", sqlalchemy.String),
    sqlalchemy.Column("year", sqlalchemy.String),
    sqlalchemy.Column("tg_id", sqlalchemy.String),
    sqlalchemy.Column("congrats_file_path", sqlalchemy.String),
)
