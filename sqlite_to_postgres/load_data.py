import logging
import sqlite3
import sqlite3 as sqlite
from dataclasses import astuple
from typing import Generator

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.db_settings import DSL
from sqlite_to_postgres.tables_db_ps import (FilmWork, FilmWorkGenre,
                                             FilmWorkPersons, Genre, Person)

logger = logging.getLogger('log.load_from_sqlite')
logger.setLevel(logging.INFO)

TABLE_TO_SCHEMA = {
    "person": Person,
    "film_work": FilmWork,
    "genre_film_work": FilmWorkGenre,
    "person_film_work": FilmWorkPersons,
    "genre": Genre,
}


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection, batch_size: int = 100):
        connection.row_factory = sqlite.Row
        self.cur = connection.cursor()
        self.batch_size = batch_size

    def get_data(self, table_name: str, schema) -> Generator[list, None, None]:
        fields = ', '.join(schema.__slots__)
        if table_name == 'person':
            fields = ', '.join(('full_name', 'birth_date', 'id',
                                'created_at', 'updated_at'))
        cursor = self.cur.execute(f"select {fields} from {table_name};""")
        while data := cursor.fetchmany(self.batch_size):
            transformed_data = self.transform(data=data, table_name=table_name,
                                              schema=schema)
            yield transformed_data

    def transform(self, data: list, table_name: str, schema):
        if table_name == 'person':
            return self.custom_transform_person(data=data)
        return [schema(*row) for row in data]

    def custom_transform_person(self, data: list):
        return [Person(
            id=person['id'],
            first_name=person['full_name'].split(' ')[0],
            last_name=' '.join(person['full_name'].split(' ')[1:]),
            patronymic=None,
            birthdate=person['birth_date'],
            created_at=person['created_at'],
            updated_at=person['updated_at']
        ) for person in data]


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.cur = pg_conn.cursor()
        self.cur.row_factory = sqlite.Row

    def create_data(self, data: Generator, table_name: str, schema) -> None:
        args_str = [astuple(film) for films in data for film in films]
        fields = ', '.join(schema.__slots__)
        values = ', '.join(['%s' for _ in range(len(schema.__slots__))])
        if table_name == 'person':
            values = '%s, %s, %s, %s, %s, %s, %s'

        INSERT_SQL = f"""
                    INSERT INTO content.{table_name}({fields})
                    VALUES ({values}) 
                    ON CONFLICT DO NOTHING;
                """

        self.cur.executemany(INSERT_SQL, tuple(args_str))


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    for table_name, schema in TABLE_TO_SCHEMA.items():
        try:
            data = sqlite_loader.get_data(table_name, schema)
            postgres_saver.create_data(data, table_name, schema)
        except Exception as exp:
            logger.info(exp)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
