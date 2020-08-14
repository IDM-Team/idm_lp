from commands import aliases
from commands import aliases_manager
from commands import delete_messages
from commands import duty_signal
from commands import members_manager
from commands import prefixes
from commands import self_signal

commands_bp = (
    self_signal.user,
    duty_signal.user,
    aliases.user,
    aliases_manager.user,
    prefixes.user,
    delete_messages.user,

    *members_manager.users_bp,
)
