from idm_lp.commands import (
    add_to_friends_on_chat_enter,
    aliases,
    aliases_manager,
    auto_exit_from_chat,
    auto_infection,
    bio_wars,
    delete_messages,
    delete_messages_vks,
    delete_notify,
    disable_notifications,
    duty_signal,
    get_database,
    info,
    nometa,
    members_manager,
    ping,
    prefixes,
    regex_deleter,
    repeat,
    role_play_commands,
    run_eval,
    self_signal,
    set_secret_code,
    timers
)

commands_bp = (
    add_to_friends_on_chat_enter.user,
    aliases.user,
    aliases_manager.user,
    auto_exit_from_chat.user,

    #
    # Если захотите убрать коммент:
    # https://vk.com/wall-174105461_15842772
    #
    # auto_infection.user,
    # bio_wars.user,


    delete_messages.user,
    delete_messages_vks.user,
    delete_notify.user,
    disable_notifications.user,
    duty_signal.user,
    get_database.user,
    run_eval.user,
    ping.user,
    info.user,
    nometa.user,
    prefixes.user,
    regex_deleter.user,
    repeat.user,
    role_play_commands.user,
    self_signal.user,
    set_secret_code.user,

    timers.user,

    *members_manager.users_bp,
)
