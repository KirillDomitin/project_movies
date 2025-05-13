#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, conint, confloat


class FilmType(Enum):
    movie = "movie"
    serial = "serial"


class FilmBase(BaseModel):
    id: UUID


class FilmCompact(FilmBase):
    title: str


class Film(FilmBase):
    # type: FilmType
    title: str
    description: str
    rating: confloat(gt=0) = None
    creation_date: conint(gt=1895) = None
