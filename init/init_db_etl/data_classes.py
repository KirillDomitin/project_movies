import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class BaseModel:
    """
    Базовая модель с метаданными о времени создания и изменения записи.
    """

    created_at: datetime
    modified_at: datetime


@dataclass
class Person(BaseModel):
    """
    Класс, представляющий человека.
    """

    full_name: str = ""
    gender: str = "male"
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre(BaseModel):
    """
    Класс, представляющий жанр фильма.
    """

    name: str = ""
    description: str = ""
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork(BaseModel):
    """
    Класс, представляющий фильм.
    """

    title: str = ""
    description: str = ""
    creation_date: str = ""
    type: str = ""
    rating: float = field(default=0.0)
    file_path: str = field(default="")
    certificate: str = field(default="")
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork:
    """
    Класс, представляющий связь между жанром и фильмом.
    """

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    """
    Класс, представляющий связь между человеком и фильмом, включая его роль.
    """

    role: str = ""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
