from typing import Dict, Any, List

from objects.base import BaseModel


class LastMessage(BaseModel):
    date: float
    from_id: int

    def save(self) -> Dict[str, Any]:
        return {
            'date': self.date,
            'from_id': self.from_id
        }


class SlouMo(BaseModel):
    chat_id: int
    last_message: LastMessage
    white_list: List[int]
    warn_message: str
    time: int

    def __init__(self, *args, **kwargs):
        super(SlouMo, self).__init__(*args, **kwargs)
        self.last_message = LastMessage(self.last_message)

    def save(self) -> Dict[str, Any]:
        return {
            'chat_id': self.chat_id,
            'last_message': self.last_message.save(),
            'white_list': self.white_list,
            'warn_message': self.warn_message,
            'time': self.time
        }
