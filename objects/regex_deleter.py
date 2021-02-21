from typing import Dict

from objects.base import BaseModel


class RegexDeleter(BaseModel):
    name: str
    regex: str
    chat_id: int
    for_all: bool

    def save(self) -> Dict[str, int]:
        return {
            'name': self.name,
            'regex': self.regex,
            'chat_id': self.chat_id,
            'for_all': self.for_all
        }
