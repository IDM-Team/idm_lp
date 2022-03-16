from typing import Optional

from vkbottle import VKError
from vkbottle.rule import ChatActionRule, FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database, ChatEnterModel
from idm_lp.rules import ChatEnterRule
from idm_lp.utils import edit_message

user = Blueprint(
    name='add_to_friends_on_chat_enter'
)


@user.on.chat_message(ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]), ChatEnterRule())
@logger_decorator
async def chat_enter_wrapper(message: Message):
    db = Database.get_current()
    model = None
    for chat_enter_model in db.add_to_friends_on_chat_enter:
        if chat_enter_model.peer_id == message.peer_id:
            model = chat_enter_model
    try:
        await user.api.friends.add(user_id=message.action.member_id)
    except VKError:
        pass
    return model.hello_text


@user.on.chat_message(FromMe(), text=[
    "<prefix:service_prefix> +добавление",
    "<prefix:service_prefix> +добавление <hello_text>"
])
@logger_decorator
async def add_chat_enter_model_wrapper(message: Message, hello_text: Optional[str] = None, **kwargs):
    db = Database.get_current()
    for i in range(len(db.add_to_friends_on_chat_enter)):
        if db.add_to_friends_on_chat_enter[i].peer_id == message.peer_id:
            db.add_to_friends_on_chat_enter[i].hello_text = hello_text
            db.save()
            await edit_message(
                message,
                "✅ Приветственный текст обновлен"
            )
            return
    db.add_to_friends_on_chat_enter.append(
        ChatEnterModel(peer_id=message.peer_id, hello_text=hello_text)
    )
    db.save()
    await edit_message(
        message,
        "✅ Добавление новичков в друзья в этом чате включено"
    )
    return


@user.on.chat_message(FromMe(), text=[
    "<prefix:service_prefix> -добавление",
])
@logger_decorator
async def add_chat_enter_model_wrapper(message: Message, **kwargs):
    with Database.get_current() as db:
        model = None
        for i in range(len(db.add_to_friends_on_chat_enter)):
            if db.add_to_friends_on_chat_enter[i].peer_id == message.peer_id:
                model = db.add_to_friends_on_chat_enter[i]
        if model is None:
            await edit_message(
                message,
                "⚠ Добавление новичков в друзья в этом чате не настроено"
            )
            return
        db.add_to_friends_on_chat_enter.remove(model)
    await edit_message(
        message,
        "✅ Добавление новичков в друзья в этом чате выключено"
    )
    return
