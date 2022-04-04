from enum import Enum

from pydantic import BaseModel, validator


class GenEnum(Enum):
    NOM = "nom"
    GEN = "gen"
    DAT = "dat"
    ACC = "acc"
    INS = "ins"
    ABL = "abl"


class RolePlayCommand(BaseModel):
    name: str
    gen: GenEnum
    formatter_man: str
    formatter_woman: str
    all_ending: str

    @validator('name')
    def to_lower_validator(cls, v: str) -> str:
        return v.lower()
