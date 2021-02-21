from commands import add_to_friends_on_chat_enter
from commands import aliases
from commands import aliases_manager
from commands import auto_exit_from_chat
from commands import delete_messages
from commands import delete_notify
from commands import disable_notifications
from commands import duty_signal
from commands import info
from commands import members_manager
from commands import ping
from commands import prefixes
from commands import regex_deleter
from commands import repeat
from commands import role_play_commands
from commands import run_eval
from commands import self_signal
from commands import set_secret_code
from commands import sloumo

commands_bp = (
    add_to_friends_on_chat_enter.user,
    aliases.user,
    aliases_manager.user,
    auto_exit_from_chat.user,
    delete_messages.user,
    delete_notify.user,
    disable_notifications.user,
    duty_signal.user,
    run_eval.user,
    ping.user,
    info.user,
    prefixes.user,
    regex_deleter.user,
    repeat.user,
    role_play_commands.user,
    self_signal.user,
    set_secret_code.user,
    sloumo.user,

    *members_manager.users_bp,
)
