from typing import Dict

from objects import DotDict

__all__ = (
    'IgnoredMembers',
    'IgnoredGlobalMembers',
    'MutedMembers',
)


class IgnoredMembers(DotDict):
    member_id: int
    chat_id: int

    def save(self) -> Dict[str, int]:
        return {
            'member_id': self.member_id,
            'chat_id': self.chat_id,
        }


class IgnoredGlobalMembers(DotDict):
    member_id: int

    def save(self) -> Dict[str, int]:
        return {
            'member_id': self.member_id,
        }


class MutedMembers(DotDict):
    member_id: int
    chat_id: int

    def save(self) -> Dict[str, int]:
        return {
            'member_id': self.member_id,
            'chat_id': self.chat_id,
        }
