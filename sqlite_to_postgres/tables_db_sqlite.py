from dataclasses import dataclass

from typing import List


@dataclass
class Actors:
    id: int
    name: str


@dataclass
class MoviesActors:
    movie_id: str
    actor_id: str


@dataclass
class Movies:
    genre: List
    director: str
    writer: str
    plot: str
    title: str
    ratings: str
    imdb_rating: str
    writers: List[dict]
    id: str
    actors: List[Actors] = None


@dataclass
class RatingAgency:
    id: str
    name: str


@dataclass
class Writers:
    id: str
    name: str
