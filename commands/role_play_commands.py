from typing import Optional

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import RolePlayCommand, Database
from utils import edit_message

user = Blueprint(
    name='role_play_commands_blueprint'
)


async def get_role_play_message(
        message: Message,
        role_play_command: RolePlayCommand,
        user_id: Optional[int] = None,
        call_all: bool = False
) -> str:
    called_user = (await message.api.users.get(fields=["sex"]))[0]

    pattern = role_play_command.formatter_woman if called_user.sex == 1 else role_play_command.formatter_man

    first_user = f"[id{called_user.id}|{called_user.first_name} {called_user.last_name}]"
    if call_all:
        return pattern.format(
            first_user=first_user,
            second_user=role_play_command.all_ending
        )

    second_user = (await message.api.users.get(user_ids=user_id, name_case=role_play_command.gen))[0]
    last_user = f"[id{second_user.id}|{second_user.first_name} {second_user.last_name}]"
    return pattern.format(
        first_user=first_user,
        second_user=last_user
    )


all_role_play_cmd = [
    "<service_prefix:service_prefix> <role_play_command:role_play_command> всех",
    "<service_prefix:service_prefix> <role_play_command:role_play_command> всем",
]


@user.on.message_handler(FromMe(), text="<service_prefix:service_prefix> рп")
async def show_rp_commands(message: Message, **kwargs):
    db = Database.get_current()
    text = "📃 Доступные РП-команды:\n"
    index = 1
    for rp_cmd in db.role_play_commands:
        text += f"{index}. {rp_cmd.name}\n"
        index += 1
    await edit_message(
        message,
        text
    )


@user.on.message_handler(FromMe(), text=all_role_play_cmd)
@logger_decorator
async def role_play_command_wrapper(
        message: Message,
        role_play_command: RolePlayCommand,
        **kwargs
):
    await edit_message(
        message,
        await get_role_play_message(
            message,
            role_play_command,
            call_all=True
        )
    )


user_id_cmd = "<service_prefix:service_prefix> <role_play_command:role_play_command> [id<user_id:int>|<name>]"


@user.on.message_handler(FromMe(), text=user_id_cmd)
@logger_decorator
async def role_play_command_wrapper(
        message: Message,
        role_play_command: RolePlayCommand,
        user_id: int,
        **kwargs
):
    await edit_message(
        message,
        await get_role_play_message(
            message,
            role_play_command,
            user_id=user_id
        )
    )


no_user_id_cmd = "<service_prefix:service_prefix> <role_play_command:role_play_command>"


@user.on.message_handler(FromMe(), text=no_user_id_cmd)
@logger_decorator
async def role_play_command_wrapper(
        message: Message,
        role_play_command: RolePlayCommand,
        **kwargs
):
    user_id = None
    if message.reply_message:
        user_id = message.reply_message.from_id
    if message.fwd_messages:
        user_id = message.fwd_messages[0].from_id

    if not user_id:
        return

    if user_id < 0:
        return

    await edit_message(
        message,
        await get_role_play_message(
            message,
            role_play_command,
            user_id=user_id
        )
    )
