import typing

from pydantic import BaseModel, validator

__all__ = (
    'IgnoredMembers',
    'MutedMembers',
)


class IgnoredMembers(BaseModel):
    member_id: int
    chat_id: typing.Optional[int]


class MutedMembers(BaseModel):
    member_id: int
    chat_id: int
    delay: int = 0

    @validator('delay')
    def positive_int_validator(cls, v: int) -> int:
        return int(v) if v > 0 else 0
