from typing import List, Callable

from objects import (
    IgroredMembers,
    IgroredGlobalMembers,
    MutedMembers,
    Alias
)


class Loaders:
    loaders: List[Callable] = []

    def __init__(self):
        self.loaders.append(self.igrored_members)
        self.loaders.append(self.igrored_global_members)
        self.loaders.append(self.muted_members)
        self.loaders.append(self.aliases)

    def __call__(self, *args, **kwargs):
        return self.loaders

    @staticmethod
    def igrored_members(data: dict) -> List[IgroredMembers]:
        return [
            IgroredMembers(ign_member)
            for ign_member in data['igrored_members']
        ]

    @staticmethod
    def igrored_global_members(data: dict) -> List[IgroredGlobalMembers]:
        return [
            IgroredGlobalMembers(ign_member)
            for ign_member in data['igrored_global_members']
        ]

    @staticmethod
    def muted_members(data: dict) -> List[MutedMembers]:
        return [
            MutedMembers(muted_member)
            for muted_member in data['muted_members']
        ]

    @staticmethod
    def aliases(data: dict) -> List[Alias]:
        return [
            Alias(alias)
            for alias in data['aliases']
        ]
