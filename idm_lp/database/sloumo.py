from typing import Dict, Any, List

from pydantic import BaseModel


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

