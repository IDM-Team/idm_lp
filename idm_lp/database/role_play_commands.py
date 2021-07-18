from typing import Dict
from pydantic import BaseModel
from enum import Enum


class GenEnum(Enum):
    NOM = "nom"
    GEN = "gen"
    DAT = "dat"
    ACC = "acc"
    INS = "ins"
    ABL = "abl"


class RolePlayCommand(BaseModel):
    """
        :param name: Имя РПшки
        :param gen: Падеж в какой возводить РПшку
        :param formatter_man: форматтер при вызове одиночной РП (обнять @lllordralll)
        :param formatter_woman: форматтер при вызове одиночной РП (обнять @lllordralll)
            Должен содержать {first_user} {second_user}
        :param all_ending: заменяет {second_user}
    """
    name: str
    gen: GenEnum
    formatter_man: str
    formatter_woman: str
    all_ending: str
