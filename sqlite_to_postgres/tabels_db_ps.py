import uuid
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Person:
    first_name: str
    last_name: str
    patronymic: str
    birthdate: date
    id: uuid.UUID


@dataclass
class FilmWork:
    title: str
    description: str
    imdb_rating: float
    ratings: str
    type: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    title: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWorkGenre:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID


@dataclass
class FilmWorkPersons:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    type_person: str
