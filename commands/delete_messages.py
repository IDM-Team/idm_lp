from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message
import rules

from objects import Database, Alias
from utils import edit_message

user = Blueprint(
    name='delete_messages_blueprint'
)


@user.on.message(rules.IgroredMembersRule())
@user.on.chat_message(rules.IgroredMembersRule())
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id]
    )


@user.on.message(rules.IgroredGlobalMembersRule())
@user.on.chat_message(rules.IgroredGlobalMembersRule())
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id]
    )


@user.on.message(rules.MutedMembersRule())
@user.on.chat_message(rules.MutedMembersRule())
async def ignore_delete_message_wrapper(message: Message):
    await message.api.messages.delete(
        message_ids=[message.id],
        delete_for_all=True
    )
