import sqlite3
from dataclasses import astuple
from pprint import pprint
from typing import List, Tuple

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.db_settings import DSL
from sqlite_to_postgres.tabels_db_ps import (FilmWork, FilmWorkGenre,
                                             FilmWorkPersons, Genre, Person)


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection):
        self.cur = connection.cursor()

    def _get_person(self, limit: int, offset: int) -> List[Person]:
        result = self.cur.execute(
            "select * from person limit :limit offset :offset",
            dict(limit=limit, offset=offset))
        return [Person(
            id=person[0],
            first_name=person[1].split(' ')[0],
            last_name=' '.join(person[1].split(' ')[1:]),
            patronymic=None,
            birthdate=person[2],
            created_at=person[3],
            updated_at=person[4]
        ) for person in result]

    def _get_genres(self, limit: int, offset: int) -> List[Genre]:
        result = self.cur.execute(
            "select * from genre limit :limit offset :offset",
            dict(limit=limit, offset=offset))
        return [Genre(
            id=genre[0],
            name=genre[1],
            description=genre[2],
            created_at=genre[3],
            updated_at=genre[4]
        ) for genre in result]

    def _get_genre_film_work(self, limit: int, offset: int) \
            -> List[FilmWorkGenre]:
        result = self.cur.execute(
            "select * from genre_film_work limit :limit offset :offset",
            dict(limit=limit, offset=offset))
        return [FilmWorkGenre(
            id=genre[0],
            film_work_id=genre[1],
            genre_id=genre[2],
            created_at=genre[3]
        ) for genre in result]

    def _get_person_film_work(self, limit: int, offset: int) \
            -> List[FilmWorkPersons]:
        result = self.cur.execute(
            "select * from person_film_work limit :limit offset :offset",
            dict(limit=limit, offset=offset))
        return [FilmWorkPersons(
            id=person[0],
            film_work_id=person[1],
            person_id=person[2],
            role=person[3],
            created_at=person[4]
        ) for person in result]

    def _get_film_work(self, limit: int, offset: int) -> List[FilmWork]:
        result = self.cur.execute(
            "select * from film_work limit :limit offset :offset",
            dict(limit=limit, offset=offset))
        return [FilmWork(
            id=film[0],
            title=film[1],
            description=film[2],
            creation_date=film[3],
            certificate=film[4],
            file_path=film[5],
            rating=film[6],
            type=film[7],
            created_at=film[8],
            updated_at=film[9]
        ) for film in result]

    def load_movies(self, limit: int, offset: int) -> Tuple:
        return (
            self._get_person(limit, offset),
            self._get_film_work(limit, offset),
            self._get_genre_film_work(limit, offset),
            self._get_person_film_work(limit, offset),
            self._get_genres(limit, offset)
        )


class PostgresSaver:

    def __init__(self, pg_conn: _connection):
        self.cur = pg_conn.cursor()

    def _insert_film(self, film_work: List[FilmWork]) -> None:
        for film in film_work:
            insert = """
                INSERT INTO content.film_work(title, description, creation_date, 
                rating, certificate, file_path, type, created_at, updated_at, id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(film))

    def _insert_persons(self, persons: List[Person]) -> None:
        for person in persons:
            insert = """
                INSERT INTO content.person(first_name, last_name, patronymic, birthdate, id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(person))

    def _insert_film_person(self, film_persons: List[FilmWorkPersons]) -> None:
        for person in film_persons:
            insert = """
                INSERT INTO content.person_film_work(film_work_id, person_id, role, created_at, id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(person))

    def _insert_genre(self, genre: List[Genre]) -> None:
        for genre in genre:
            insert = """
                INSERT INTO content.genre(name, description, id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(genre))

    def _insert_genre_film_work(self, genre_film: List[FilmWorkGenre]) -> None:
        for genre_film in genre_film:
            insert = """
                INSERT INTO content.genre_film_work(film_work_id, genre_id, created_at, id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(genre_film))

    def truncate(self):
        for table in ["film_work", "genre_film_work", "person_film_work",
                      "genre", "person"]:
            self.cur.execute("TRUNCATE content.{} CASCADE;".format(table))

    def save_all_data(self, data: Tuple):
        insert_operation = (
            self._insert_persons,
            self._insert_film,
            self._insert_genre_film_work,
            self._insert_film_person,
            self._insert_genre
        )
        for tale_data, insert_method in zip(data, insert_operation):
            try:
                insert_method(tale_data)
            except Exception as ex:
                pprint(ex)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    cur = connection.cursor()

    cur.execute("select count(*) from film_work")
    film_work_count, = cur.fetchone()
    cur.execute("select count(*) from genre")
    genre_count, = cur.fetchone()
    cur.execute("select count(*) from genre_film_work")
    genre_film_work_count, = cur.fetchone()
    cur.execute("select count(*) from person")
    person_count, = cur.fetchone()
    cur.execute("select count(*) from person_film_work")
    person_film_work_count, = cur.fetchone()

    max_count = max(film_work_count, genre_count, genre_film_work_count,
                    person_film_work_count, person_count)
    limit = 100
    for total in range(0, max_count, 100):
        offset = total
        data = sqlite_loader.load_movies(limit=limit, offset=offset)
        postgres_saver.save_all_data(data)
        limit += 100


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
