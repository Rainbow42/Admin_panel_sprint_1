import uuid
from dataclasses import dataclass
from datetime import date


@dataclass
class Person:
    __slots__ = ('first_name', 'last_name', 'patronymic', 'birthdate', 'id',
                 'created_at', 'updated_at')
    first_name: str
    last_name: str
    patronymic: str
    birthdate: date
    id: uuid.UUID
    created_at: date
    updated_at: date


@dataclass
class FilmWork:
    __slots__ = ('title', 'description', 'creation_date', 'rating', 'id',
                 'certificate', 'file_path', 'type', 'created_at', 'updated_at')
    title: str
    description: str
    creation_date: date
    rating: float
    certificate: str
    file_path: str
    type: str
    created_at: date
    updated_at: date
    id: uuid.UUID


@dataclass
class Genre:
    __slots__ = ('name', 'description', 'id', 'created_at', 'updated_at')
    name: str
    description: str
    id: uuid.UUID
    created_at: date
    updated_at: date


@dataclass
class FilmWorkGenre:
    __slots__ = ('film_work_id', 'genre_id', 'created_at', 'id')
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: date
    id: uuid.UUID


@dataclass
class FilmWorkPersons:
    __slots__ = ('film_work_id', 'person_id', 'role', 'created_at', 'id')
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: date
    id: uuid.UUID
