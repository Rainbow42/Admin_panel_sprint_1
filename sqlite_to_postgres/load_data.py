import json
import sqlite3
from dataclasses import astuple
from datetime import datetime
from typing import List, Union

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.db_settings import DSL
from sqlite_to_postgres.tabels_db_ps import FilmWork, FilmWorkGenre, Genre, \
    Person, FilmWorkPersons
from sqlite_to_postgres.tables_db_sqlite import Movies, FilmRoles


class SQLiteLoader:
    """Выгружает данные из бд и нормализуется под новую схему"""
    actors = dict()  # можно было бы создать словарь person,
    # но деление в дальнейшем упростит проставление enum
    writers = dict()
    genre = dict()
    directions = dict()

    def __init__(self, connection: sqlite3.Connection):
        self.cur = connection.cursor()

    def _duplicate_protection(self, person: FilmRoles) -> Union[
        FilmRoles, None]:
        # используем словарь чтобы не создавать в дальнейшем дубли
        if person_hash := self.actors.get(person.name):
            return person_hash
        elif person_hash := self.writers.get(person.name):
            return person_hash
        elif person_hash := self.directions.get(person.name):
            return person_hash
        return None

    def _get_writers(self, movie: Movies):
        if not movie.writers:
            return list()

        writers_ids = list()
        writers = json.loads(movie.writers)
        for writer in writers:
            writers_ids.append(writer.get("id"))
        result_query = self.cur.execute(
            f"select name from writers where id in {tuple(writers_ids)};")
        writers = set(result_query.fetchall())

        result = list()
        for name in writers:
            if name[0] == 'N/A':
                continue
            writer = FilmRoles(name=name[0])
            writer.id = str(writer.id)
            person = self._duplicate_protection(writer)
            if not person:
                self.writers[writer.name] = writer
                result.append(writer)
                continue
            result.append(person)
        return result

    def _get_writer(self, movie: Movies) -> Union[FilmRoles, None]:
        if not movie.writer:
            return None
        result = self.cur.execute(
            "select name from writers where id=:writer_id;",
            dict(writer_id=movie.writer))
        writer = result.fetchall()
        if writer[0][0] == 'N/A':
            return None
        writer = FilmRoles(name=writer[0][0])
        writer.id = str(writer.id)
        # берем из словаря что не создать дублей в бд
        person = self._duplicate_protection(writer)
        if not person:
            self.directions[writer.name] = writer
            return writer
        return person

    def _get_actor(self, movie: Movies) -> Union[List[FilmRoles], None]:
        result = self.cur.execute(
            "select actor_id from movie_actors where movie_id = :movie_id",
            dict(movie_id=movie.id))
        actor_ids = result.fetchall()
        if not actor_ids:
            return None
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
            return list()

        result = list()
        for actor in actors:
            actor = FilmRoles(name=actor[0])
            actor.id = str(actor.id)
            person = self._duplicate_protection(actor)
            if not person:
                self.actors[actor.name] = actor
                result.append(actor)
                continue
            result.append(person)
        return result

    def _get_genres(self, movie: Movies) -> List:
        result = list()
        genres = [genre.replace(' ', '') for genre in movie.genre.split(',')]
        for genre in set(genres):
            genre = Genre(title=genre)
            genre.id = str(genre.id)
            # используем словарь чтобы не создавать в дальнейшем дубли
            if genre_hash := self.genre.get(genre.title):
                result.append(genre_hash)
            else:
                self.genre[genre.title] = genre
                result.append(genre)

        return result

    def _get_direction(self, movie: Movies) -> Union[List[FilmRoles], None]:
        if movie.director == 'N/A':
            return None
        directions = movie.director.split(", ")
        result = list()
        for direction in directions:
            direction = FilmRoles(name=direction)
            direction.id = str(direction.id)
            person = self._duplicate_protection(direction)
            if not person:
                self.directions[direction.name] = direction
                result.append(direction)
                continue
            result.append(person)
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
            movie.director = self._get_direction(movie)
            movie.genre = self._get_genres(movie)
            movie.actors = self._get_actor(movie)
            writers_ids = self._get_writers(movie)
            writer_id = self._get_writer(movie)

            if writer_id:
                writers_ids.append(writer_id)

            movie.writers = writers_ids  # m2m
            movies.append(movie)

        return movies


class PostgresSaver:
    film_work = list()
    genre = list()
    writers_person = list()
    actors_person = list()
    direction_person = list()

    actors_film = list()
    genre_film = list()
    writer_film = list()
    direction_film = list()

    def __init__(self, pg_conn: _connection):
        self.cur = pg_conn.cursor()

    def _processing_data(self, data: list):
        for movie in data:
            # так как данные ненормальзирваные
            # и могут встречаться строки вида ('N/A')
            film = FilmWork(
                title=movie.title,
                type='film',
                description=None if movie.plot == 'N/A' else movie.plot,
                ratings=None if movie.ratings == 'N/A' else movie.ratings,
                imdb_rating=None if movie.imdb_rating == 'N/A' else float(
                    movie.imdb_rating),
            )

            film.id = str(film.id)
            if movie.director:
                for director in movie.director:
                    director_person = FilmWorkPersons(
                        film_work_id=film.id,
                        person_id=director.id,
                        type_person="directions")  # m2m

                    self.direction_film.append(director_person)

            for writer in movie.writers:  # m2m
                writer_person = FilmWorkPersons(
                    film_work_id=film.id,
                    person_id=writer.id,
                    type_person='writers'
                )
                self.writer_film.append(writer_person)

            for actor in movie.actors:  # m2m
                actor_person = FilmWorkPersons(
                    film_work_id=film.id,
                    person_id=actor.id,
                    type_person='actors'
                )
                self.actors_film.append(actor_person)

            for genre in movie.genre:  # m2m
                genre_film = FilmWorkGenre(
                    film_work_id=film.id,
                    genre_id=genre.id
                )
                self.genre_film.append(genre_film)
                self.genre.append(genre)

            self.film_work.append(film)
            self.writers_person.extend(movie.writers)
            self.actors_person.extend(movie.actors)
            if movie.director:
                self.direction_person.extend(movie.director)

    def _insert_film(self):
        for film in self.film_work:
            insert = """
                INSERT INTO content.film_work(title, description, imdb_rating, ratings, type, id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(film))

    def _insert_persons(self, persons: List[Person]):
        for person in persons:
            insert = """
                INSERT INTO content.person(first_name, last_name, patronymic, birthdate, id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(person))

    def _insert_film_person(self):
        film_persons = [*self.actors_film,
                        *self.writer_film,
                        *self.direction_film]
        for person in film_persons:
            insert = """
                INSERT INTO content.film_work_persons_type(film_work_id, person_id, type_person)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(person))

    def _insert_genre(self):
        for genre in self.genre:
            insert = """
                INSERT INTO content.genre(title, id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(genre))

        for genre_film in self.genre_film:
            insert = """
                INSERT INTO content.film_work_genre(film_work_id, genre_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """
            self.cur.execute(insert, astuple(genre_film))

    def normalization_person(self) -> List[Person]:
        normalization = list()
        persons = [*self.writers_person,
                   *self.actors_person,
                   *self.direction_person]
        for writer in persons:
            name = writer.name.split(' ')
            person = Person(
                first_name=name[0],
                last_name=" ".join(name[1:]),
                patronymic=None,
                birthdate=datetime.now().date(),
                id=writer.id
            )
            normalization.append(person)
        return normalization

    def TRUNCATE(self):
        for i in ["film_work", "film_work_genre", "film_work_persons_type","genre", "person"]:
            self.cur.execute("TRUNCATE content.{} CASCADE;".format(i))

    def save_all_data(self, data: list):
        self._processing_data(data)
        persons = self.normalization_person()

        self._insert_film()
        self._insert_persons(persons)
        self._insert_film_person()
        self._insert_genre()
        # self.TRUNCATE()


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
