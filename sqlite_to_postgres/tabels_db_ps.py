import uuid
from dataclasses import dataclass, field


@dataclass
class Person:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWorkPersons:
    film_work_id: uuid.UUID
    person_id: int


@dataclass
class FilmWork:
    director: str
    title: str
    plot: str
    ratings: int
    imdb_rating: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWorkGenre:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID


@dataclass
class Genre:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Writers:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWorkWriters:
    film_work_id: uuid.UUID
    writer_id: uuid.UUID
