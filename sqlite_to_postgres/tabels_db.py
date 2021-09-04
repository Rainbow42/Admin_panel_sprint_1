import uuid
from dataclasses import dataclass, field
from uuid import UUID
from typing import List


@dataclass
class Actors:
    id: int
    name: str


@dataclass
class MovieActors:
    movie_id: uuid.UUID
    actor_id: int


@dataclass
class Movies:
    genre: List[str]
    directors : str

    id: uuid.UUID = field(default_factory=uuid.uuid4)