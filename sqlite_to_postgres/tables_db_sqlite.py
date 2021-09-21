from dataclasses import dataclass, field

from typing import List

import uuid as uuid


@dataclass
class FilmRoles:
    name: str
    id: str = field(default_factory=uuid.uuid4)


@dataclass
class Directions:
    uuid: uuid.UUID
    name: str


@dataclass
class MoviesActors:
    movie_id: str
    actor_id: str


@dataclass
class Movies:
    genre: List
    director: List[FilmRoles]
    writer: str
    plot: str
    title: str
    ratings: str
    imdb_rating: str
    writers: List[FilmRoles]
    id: str
    actors: List[FilmRoles] = None


@dataclass
class RatingAgency:
    id: str
    name: str


@dataclass
class Writers:
    uuid: uuid.UUID
    name: str
