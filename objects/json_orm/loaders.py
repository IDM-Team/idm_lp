from typing import List, Callable

import const
from objects import (
    IgroredMembers,
    IgroredGlobalMembers,
    MutedMembers,
    Alias,
    RolePlayCommand
)

import requests


class Loaders:
    loaders: List[Callable] = []

    def __init__(self):
        self.loaders.append(self.igrored_members)
        self.loaders.append(self.igrored_global_members)
        self.loaders.append(self.muted_members)
        self.loaders.append(self.aliases)
        self.loaders.append(self.role_play_commands)

    def __call__(self, *args, **kwargs):
        return self.loaders

    @staticmethod
    def igrored_members(data: dict) -> List[IgroredMembers]:
        try:
            return [
                IgroredMembers(ign_member)
                for ign_member in data['igrored_members']
            ]
        except KeyError:
            return []

    @staticmethod
    def igrored_global_members(data: dict) -> List[IgroredGlobalMembers]:
        try:
            return [
                IgroredGlobalMembers(ign_member)
                for ign_member in data['igrored_global_members']
            ]
        except KeyError:
            return []

    @staticmethod
    def muted_members(data: dict) -> List[MutedMembers]:
        try:
            return [
                MutedMembers(muted_member)
                for muted_member in data['muted_members']
            ]

        except KeyError:
            return []

    @staticmethod
    def aliases(data: dict) -> List[Alias]:
        try:
            return [
                Alias(alias)
                for alias in data['aliases']
            ]
        except KeyError:
            return []

    @staticmethod
    def role_play_commands(data: dict) -> List[RolePlayCommand]:
        try:
            return [
                RolePlayCommand(role_play_command)
                for role_play_command in requests.get(
                    const.ROLE_PLAY_COMMANDS_REST
                ).json()['role_play_commands']
            ]
        except:
            return []
