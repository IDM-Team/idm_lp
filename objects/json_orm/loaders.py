from typing import List, Callable

import const
from objects import (
    IgnoredMembers,
    IgnoredGlobalMembers,
    MutedMembers,
    Alias,
    RolePlayCommand
)

import requests

from objects.sloumo import SlouMo


class Loaders:
    loaders: List[Callable] = []

    def __init__(self):
        self.loaders.append(self.ignored_members)
        self.loaders.append(self.ignored_global_members)
        self.loaders.append(self.muted_members)
        self.loaders.append(self.aliases)
        self.loaders.append(self.role_play_commands)
        self.loaders.append(self.sloumo)

    def __call__(self, *args, **kwargs):
        return self.loaders

    @staticmethod
    def ignored_members(data: dict) -> List[IgnoredMembers]:
        try:
            return [
                IgnoredMembers(ign_member)
                for ign_member in data['ignored_members']
            ]
        except KeyError:
            return []

    @staticmethod
    def sloumo(data: dict) -> List[SlouMo]:
        try:
            return [
                SlouMo(slou)
                for slou in data['sloumo']
            ]
        except KeyError:
            return []

    @staticmethod
    def ignored_global_members(data: dict) -> List[IgnoredGlobalMembers]:
        try:
            return [
                IgnoredGlobalMembers(ign_member)
                for ign_member in data['ignored_global_members']
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
            role_play_commands = requests.get(
                const.ROLE_PLAY_COMMANDS_REST
            ).json()['role_play_commands'] if const.ROLE_PLAY_COMMANDS_USE_REST else data['role_play_commands']

            return [
                RolePlayCommand(role_play_command)
                for role_play_command in
                role_play_commands
            ]
        except KeyError:
            return []
