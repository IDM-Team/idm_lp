from typing import Dict
from pydantic import BaseModel

__all__ = (
    'IgnoredMembers',
    'IgnoredGlobalMembers',
    'MutedMembers',
)


class IgnoredMembers(BaseModel):
    member_id: int
    chat_id: int


class IgnoredGlobalMembers(BaseModel):
    member_id: int


class MutedMembers(BaseModel):
    member_id: int
    chat_id: int
    delay: int = 0
