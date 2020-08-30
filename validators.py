from vbml.blanket import validator
from objects import Database

__all__ = (
    'alias',
    'role_play_command',
    'self_prefix',
    'duty_prefix',
    'service_prefix',
)


@validator
def alias(value: str):
    db = Database.get_current()
    for alias_ in db.aliases:
        if value.lower() == alias_.command_from:
            return alias_


@validator
def role_play_command(value: str):
    db = Database.get_current()
    for rp_cmd in db.role_play_commands:
        if value.lower() == rp_cmd.name.lower():
            return rp_cmd


@validator
def self_prefix(value: str):
    db = Database.get_current()
    if value.lower() in db.self_prefixes:
        return value


@validator
def duty_prefix(value: str):
    db = Database.get_current()
    if value.lower() in db.duty_prefixes:
        return value


@validator
def service_prefix(value: str):
    db = Database.get_current()
    if value.lower() in db.service_prefixes:
        return value
