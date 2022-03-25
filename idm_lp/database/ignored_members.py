import typing

from pydantic import BaseModel

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
