import json
import sqlite3
from dataclasses import astuple
from pprint import pprint
from typing import List

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.db_settings import DSL
from sqlite_to_postgres.tabels_db_ps import FilmWork, FilmWorkGenre, Genre, \
    Writers, FilmWorkWriters, Person, FilmWorkPersons
from sqlite_to_postgres.tables_db_sqlite import Movies


class SQLiteLoader:
    actors = dict()
    writers = dict()
    genre = dict()

    def __init__(self, connection: sqlite3.Connection):
        self.cur = connection.cursor()

    def _get_writers(self, movie: Movies):
        writers_ids = list()
        if not movie.writers:
            return list()

        writers = json.loads(movie.writers)
        for writer in writers:
            writers_ids.append(writer.get("id"))
        result = self.cur.execute(
            f"select name from writers where id in {tuple(writers_ids)};")
        writers = set(result.fetchall())

        result = list()
        for name in writers:
            if name[0] == 'N/A':
                continue
            writer = Writers(name=name[0])
            writer.id = str(writer.id)
            if writer_hash := self.writers.get(writer.name):
                result.append(writer_hash)
            else:
                self.writers[writer.name] = writer
                result.append(writer)
        return result

    def _get_writer(self, movie: Movies):
        if not movie.writer:
            return
        result = self.cur.execute(
            "select name from writers where id=:writer_id;",
            dict(writer_id=movie.writer))
        writer = result.fetchall()
        if writer[0][0] == 'N/A':
            return
        writer = Writers(name=writer[0][0])
        writer.id = str(writer.id)
        # берем из словаря что не создать дублей в бд
        if writer_hash := self.writers.get(writer.name):
            writer = writer_hash
        else:
            self.writers[writer.name] = writer
        return writer

    def _get_actor(self, movie: Movies) -> List:
        result = self.cur.execute(
            "select actor_id from movie_actors where movie_id = :movie_id",
            dict(movie_id=movie.id))
        actor_ids = result.fetchall()
        if not actor_ids:
            return
        actors_ids = list()
        for id in actor_ids:
            actors_ids.append(str(id[0][0]))

        if len(actors_ids) >= 2:
            result = self.cur.execute(
                f"select name from actors where id in {tuple(actors_ids)};")
        else:
            result = self.cur.execute(
                f"select name from actors where id = {actors_ids[0]};")

        actors = result.fetchall()
        if not actors:
            return
        result = list()
        for actor in actors:
            pprint(actor[0])
            person = Person(name=actor[0])
            person.id = str(person.id)
            # используем словарь чтобы не создавать в дальнейшем дубли
            if person_hash := self.actors.get(person.name):
                result.append(person_hash)
            else:
                self.actors[person.name] = person
                result.append(person)
        return result

    def _get_genres(self, movie: Movies) -> List:
        result = list()
        genres = [genre.replace(' ', '') for genre in movie.genre.split(',')]
        for genre in set(genres):
            genre = Genre(name=genre)
            genre.id = str(genre.id)
            # используем словарь чтобы не создавать в дальнейшем дубли
            if genre_hash := self.genre.get(genre.name):
                result.append(genre_hash)
            else:
                self.genre[genre.name] = genre
                result.append(genre)

        return result

    def load_movies(self):
        result = self.cur.execute("select * from movies;")
        movies = list()
        for rows in result.fetchall():
            movie = Movies(
                id=rows[0],
                genre=rows[1],
                director=rows[2],
                writer=rows[3],
                title=rows[4],
                plot=rows[5],
                ratings="NULL" if not rows[6] else rows[6],
                imdb_rating=rows[7],
                writers=rows[8]
            )
            movie.genre = self._get_genres(movie)
            movie.actors = self._get_actor(movie)
            writers_ids = self._get_writers(movie)
            writer_id = self._get_writer(movie)
            if writer_id:
                writers_ids.append(writer_id)

            movie.writers = writers_ids
            movies.append(movie)

        return movies


class PostgresSaver:
    film_work = list()
    genre = list()
    genre_film = list()
    writer_film = list()
    writers = list()
    actors_film = list()
    actors = list()

    def __init__(self, pg_conn: _connection):
        self.cur = pg_conn.cursor()

    def _processing_data(self, data: list):
        for movie in data:
            # так как данные ненормальзирваные
            # и могут встречаться строки вида ('N/A')
            film = FilmWork(
                director=None if movie.director == 'N/A' else movie.director,
                title=None if movie.title == 'N/A' else movie.title,
                plot=None if movie.plot == 'N/A' else movie.plot,
                ratings=None if movie.ratings == 'N/A' else movie.ratings,
                imdb_rating=None if movie.imdb_rating == 'N/A' else float(
                    movie.imdb_rating),
            )
            film.id = str(film.id)
            for genre in movie.genre:
                self.genre_film.append(FilmWorkGenre(
                    film_work_id=film.id, genre_id=genre.id))

            for writer in movie.writers:
                self.writer_film.append(FilmWorkWriters(
                    film_work_id=film.id, writer_id=writer.id))

            for actor in movie.actors:
                self.actors_film.append(FilmWorkPersons(
                    film_work_id=film.id, person_id=actor.id))

            self.film_work.append(film)
            self.genre.append(genre)
            self.writers.extend(movie.writers)
            self.actors.extend(movie.actors)

    def _insert_writers(self):
        for writer in self.writers:
            insert = """INSERT INTO content.writer(name, id)
                         VALUES (%s, %s)
                         ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(writer))

        for writer_film in self.writer_film:
            insert = """INSERT INTO content.film_work_writers(film_work_id, writer_id)
                         VALUES (%s, %s)
                         ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(writer_film))

    def _insert_actors(self):
        for actor in self.actors:
            insert = """INSERT INTO content.person(name, id)
                                VALUES (%s, %s)
                                ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(actor))

        for actors_film in self.actors_film:
            insert = """INSERT INTO content.film_work_person(film_work_id, person_id)
                                VALUES (%s, %s)
                                ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(actors_film))

    def _insert_film_work(self):
        for film in self.film_work:
            insert = """INSERT INTO content.film_work(director, title, plot, ratings, imdb_rating, id)
                         VALUES (%s, %s, %s, %s, %s, %s)
                         ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(film))

    def _insert_genre(self):
        for genre in self.genre:
            insert = """INSERT INTO content.genre(name, id)
                         VALUES (%s, %s)
                         ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(genre))

        for genre_film in self.genre_film:
            insert = """INSERT INTO content.film_work_genre(film_work_id, genre_id)
                         VALUES (%s, %s)
                         ON CONFLICT DO NOTHING;"""
            self.cur.execute(insert, astuple(genre_film))

    def save_all_data(self, data: list):
        self._processing_data(data)
        self._insert_film_work()
        self._insert_genre()
        self._insert_writers()
        self._insert_actors()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
