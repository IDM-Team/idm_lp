from vkbottle.user import Blueprint, Message

import rules
from logger import logger_decorator

user = Blueprint(
    name='delete_messages_blueprint'
)


@user.on.message_handler(rules.IgnoredMembersRule())
@logger_decorator
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id]
    )


@user.on.message_handler(rules.IgnoredGlobalMembersRule())
@logger_decorator
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id]
    )


@user.on.message_handler(rules.MutedMembersRule())
@logger_decorator
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id],
        delete_for_all=True
    )
