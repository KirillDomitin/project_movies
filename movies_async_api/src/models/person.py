#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum

from pydantic import BaseModel, UUID4


class GenderEnum(str, Enum):
    male = "male"
    female = "female"


class PersonBase(BaseModel):
    id: UUID4
    full_name: str
    gender: GenderEnum


class Actor(PersonBase): ...


class Writer(PersonBase): ...


class Director(PersonBase): ...
