import asyncio

from vkbottle.user import Blueprint, Message

from idm_lp import rules
from idm_lp.logger import logger_decorator
from idm_lp.database import Database

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
async def muted_delete_message_wrapper(message: Message):
    db = Database.get_current()
    for muted_member in db.muted_members:
        if muted_member.chat_id == message.peer_id and muted_member.member_id == message.from_id:
            if muted_member.delay:
                await asyncio.sleep(muted_member.delay)
            await message.api.messages.delete(
                message_ids=[message.id],
                delete_for_all=True
            )
