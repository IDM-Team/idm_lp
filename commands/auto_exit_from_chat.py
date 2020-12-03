from vkbottle.rule import ChatActionRule, FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='auto_exit_from_chat_blueprint'
)


async def set_auto_exit(
        db: Database,
        auto_exit: bool = None,
        delete_chat: bool = None,
        black_list: bool = None
):
    db.auto_exit_from_chat = auto_exit if auto_exit is not None else db.auto_exit_from_chat
    db.auto_exit_from_chat_delete_chat = delete_chat if delete_chat is not None else db.auto_exit_from_chat_delete_chat
    db.auto_exit_from_chat_add_to_black_list = (
        black_list if black_list is not None else db.auto_exit_from_chat_add_to_black_list
    )
    db.save()


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +автовыход")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, True, False)
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -автовыход")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, False, False)
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автовыход +чс")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, black_list=True)
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автовыход -чс")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db,  black_list=False)
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автовыход +удаление")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db, delete_chat=True)
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автовыход -удаление")
@logger_decorator
async def auto_exit_setting_on_exit_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await set_auto_exit(db,  delete_chat=False)
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.chat_message(ChatActionRule("chat_invite_user"))
@logger_decorator
async def auto_exit_from_wrapper(message: Message):
    if message.action.member_id == await message.api.user_id:
        db = Database.get_current()
        if db.auto_exit_from_chat:
            await message.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=await message.api.user_id)
        if db.auto_exit_from_chat_delete_chat:
            await message.api.messages.delete_conversation(peer_id=message.peer_id)
        if db.auto_exit_from_chat_add_to_black_list:
            await message.api.account.ban(owner_id=message.from_id)
