from typing import Dict
from objects.base import BaseModel

__all__ = (
    'IgnoredMembers',
    'IgnoredGlobalMembers',
    'MutedMembers',
)


class IgnoredMembers(BaseModel):
    member_id: int
    chat_id: int

    def save(self) -> Dict[str, int]:
        return {
            'member_id': self.member_id,
            'chat_id': self.chat_id
        }


class IgnoredGlobalMembers(BaseModel):
    member_id: int

    def save(self) -> Dict[str, int]:
        return {
            'member_id': self.member_id,
        }


class MutedMembers(BaseModel):
    member_id: int
    chat_id: int
    delay: int

    def __init__(self, *args, **kwargs):
        super(MutedMembers, self).__init__(*args, **kwargs)
        self.setdefault('delay', 0)

    def save(self) -> Dict[str, int]:
        return {
            'member_id': self.member_id,
            'chat_id': self.chat_id,
            'delay': self.delay
        }
