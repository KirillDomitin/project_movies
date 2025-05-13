#!/usr/bin/python
# -*- coding: utf-8 -*-
from pydantic import BaseModel, UUID4


class GenreBase(BaseModel):
    id: UUID4


class Genre(GenreBase):
    name: str
    description: str
