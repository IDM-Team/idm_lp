from commands import aliases
from commands import aliases_manager
from commands import delete_messages
from commands import duty_signal
from commands import members_manager
from commands import ping
from commands import prefixes
from commands import self_signal

commands_bp = (
    aliases.user,
    aliases_manager.user,
    delete_messages.user,
    duty_signal.user,
    ping.user,
    prefixes.user,
    self_signal.user,

    *members_manager.users_bp,
)
