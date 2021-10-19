import logging
import sqlite3
import sqlite3 as sqlite
from dataclasses import astuple
from sqlite3 import Cursor

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.db_settings import DSL
from sqlite_to_postgres.tabels_db_ps import (FilmWork, FilmWorkGenre,
                                             FilmWorkPersons, Genre, Person)

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection):
        connection.row_factory = sqlite.Row
        self.cur = connection.cursor()

    def get_data(self, name: str) -> Cursor:
        return self.cur.execute(f"select * from {name};""")

    def _get_person(self, persons: list) -> list[Person]:
        return [Person(
            id=person['id'],
            first_name=person['full_name'].split(' ')[0],
            last_name=' '.join(person['full_name'].split(' ')[1:]),
            patronymic=None,
            birthdate=person['birth_date'],
            created_at=person['created_at'],
            updated_at=person['updated_at']
        ) for person in persons]

    def _get_genres(self, genres: list) -> list[Genre]:
        return [Genre(
            id=genre['id'],
            name=genre['name'],
            description=genre['description'],
            created_at=genre['created_at'],
            updated_at=genre['updated_at']
        ) for genre in genres]

    def _get_genre_film_work(self, genres: list) -> list[FilmWorkGenre]:
        return [FilmWorkGenre(
            id=genre['id'],
            film_work_id=genre['film_work_id'],
            genre_id=genre['genre_id'],
            created_at=genre['created_at']
        ) for genre in genres]

    def _get_person_film_work(self, persons: list) -> list[FilmWorkPersons]:
        return [FilmWorkPersons(
            id=person['id'],
            film_work_id=person["film_work_id"],
            person_id=person["person_id"],
            role=person["role"],
            created_at=person["created_at"]
        ) for person in persons]

    def _get_film_work(self, films_work: list) -> list[FilmWork]:
        return [FilmWork(
            id=film['id'],
            title=film['title'],
            description=film['description'],
            creation_date=film['creation_date'],
            certificate=film['certificate'],
            file_path=film['file_path'],
            rating=film['rating'],
            type=film['type'],
            created_at=film['created_at'],
            updated_at=film['updated_at']
        ) for film in films_work]


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.cur = pg_conn.cursor()
        self.cur.row_factory = sqlite.Row

    def create_data(self, sql_query: str, data: tuple) -> None:
        args_str = (astuple(film) for film in data)
        self.cur.executemany(sql_query, args_str)

    INSERT_FILM = """
        INSERT INTO content.film_work(title, description, creation_date,
        rating, certificate, file_path, type, created_at, updated_at, id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON CONFLICT DO NOTHING;
    """
    INSERT_PERSON = """
        INSERT INTO content.person(first_name, last_name, 
        patronymic, birthdate, id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
    """
    INSERT_PERSON_FILM_WORK = """
        INSERT INTO content.person_film_work(film_work_id, person_id, role,
        created_at, id)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
     """
    INSERT_GENRE = """
        INSERT INTO content.genre(name, description, id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
     """
    INSERT_GENRE_FILM_WORK = """
    INSERT INTO content.genre_film_work(film_work_id, genre_id, created_at, id)
    VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING; 
    """


def save_all_data(name, sqlite_loader, get_data, postgres_saver, insert_method):
    cur_sqlite = sqlite_loader.get_data(name)
    while True:
        data_table = cur_sqlite.fetchmany(100)
        if not data_table:
            break
        method = getattr(sqlite_loader, get_data)
        data_class = method(data_table)

        insert_sql = getattr(postgres_saver, insert_method)
        postgres_saver.create_data(insert_sql, data_class)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    get_data_class = (
        "_get_person",
        "_get_film_work",
        "_get_genre_film_work",
        "_get_person_film_work",
        "_get_genres"
    )

    table_name = ("person", "film_work", "genre_film_work",
                  "person_film_work", "genre")

    insert_operation = (
        "INSERT_PERSON",
        "INSERT_FILM",
        "INSERT_GENRE_FILM_WORK",
        "INSERT_PERSON_FILM_WORK",
        "INSERT_GENRE",
    )
    for name, get_data, insert_method in zip(table_name, get_data_class,
                                             insert_operation):
        try:
            save_all_data(name, sqlite_loader, get_data, postgres_saver,
                          insert_method)
        except Exception as ex:
            logging.info(ex)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
