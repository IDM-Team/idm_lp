from typing import Optional

from objects.base import BaseModel


class ChatEnterModel(BaseModel):
    peer_id: int
    hello_text: Optional[str]

    def save(self):
        return {
            "peer_id": self.peer_id,
            "hello_text": self.hello_text
        }
