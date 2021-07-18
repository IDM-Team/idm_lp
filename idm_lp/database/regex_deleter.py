from pydantic import BaseModel


class RegexDeleter(BaseModel):
    name: str
    regex: str
    chat_id: int
    for_all: bool = False
