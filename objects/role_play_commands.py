from typing import Dict
from objects.base import BaseModel


class RolePlayCommand(BaseModel):
    """
        :param name: Имя РПшки
        :param gen: Падеж в какой возводить РПшку
            nom — именительный;
            gen — родительный;
            dat — дательный;
            acc — винительный;
            ins — творительный;
            abl — предложный.
        :param formatter_man: форматтер при вызове одиночной РП (обнять @lllordralll)
        :param formatter_woman: форматтер при вызове одиночной РП (обнять @lllordralll)
            Должен содержать {first_user} {second_user}
        :param all_ending: заменяет {second_user}
    """
    name: str
    gen: str
    formatter_man: str
    formatter_woman: str
    all_ending: str

    def save(self) -> Dict[str, str]:
        return {
            'name': self.name,
            'gen': self.gen,
            'formatter_man': self.formatter_man,
            'formatter_woman': self.formatter_woman,
            'all_ending': self.all_ending,
        }
