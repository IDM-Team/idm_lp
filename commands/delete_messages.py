from vkbottle.user import Blueprint, Message

import rules
from logger import logger_decorator

user = Blueprint(
    name='delete_messages_blueprint'
)


@user.on.message(rules.IgroredMembersRule())
@user.on.chat_message(rules.IgroredMembersRule())
@logger_decorator
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id]
    )


@user.on.message(rules.IgroredGlobalMembersRule())
@user.on.chat_message(rules.IgroredGlobalMembersRule())
@logger_decorator
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id]
    )


@user.on.message(rules.MutedMembersRule())
@user.on.chat_message(rules.MutedMembersRule())
@logger_decorator
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id],
        delete_for_all=True
    )
