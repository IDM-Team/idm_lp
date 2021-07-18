from typing import Optional

from pydantic import BaseModel


class ChatEnterModel(BaseModel):
    peer_id: int
    hello_text: Optional[str]
