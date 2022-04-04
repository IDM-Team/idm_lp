from pydantic import BaseModel, validator


class RegexDeleter(BaseModel):
    name: str
    regex: str
    chat_id: int
    for_all: bool = False

    @validator('name')
    def to_lower_validator(cls, v: str) -> str:
        return v.lower()
