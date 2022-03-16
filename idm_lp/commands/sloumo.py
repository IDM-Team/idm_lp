import time

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database, LastMessage, SlouMo
from idm_lp.rules import SlouMoRule
from idm_lp.utils import edit_message

user = Blueprint(
    name='sloumo_blueprint'
)


@user.on.chat_message(SlouMoRule())
async def sloumo_proc_wrapper(message: Message):
    if message.from_id < 0:
        return

    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i

    if (
            message.from_id not in db.sloumo[index].white_list and
            db.sloumo[index].last_message.date + db.sloumo[index].time >= time.time() and
            db.sloumo[index].last_message.from_id == message.from_id
    ):
        await message.reply(f"!warn @id{message.from_id}\n{db.sloumo[index].warn_message}")

    db.sloumo[index].last_message = LastMessage(
        date=message.date,
        from_id=message.from_id
    )
    db.save()


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +слоумо <delay_time:int>\n<warn_text>")
@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +слоумо <delay_time:int>")
@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +слоумо")
@logger_decorator
async def enable_sloumo_wrapper(
        message: Message,
        delay_time: int = 10,
        warn_text: str = "Нарушение слоумо-режима",
        **kwargs
):
    with Database.get_current() as db:
        sloumo_item = None
        for _sloumo_item in db.sloumo:
            if _sloumo_item.chat_id == message.chat_id:
                sloumo_item = _sloumo_item
        if sloumo_item is not None:
            db.sloumo.remove(sloumo_item)
        db.sloumo.append(SlouMo(
            chat_id=message.chat_id,
            last_message=LastMessage(from_id=0, date=0),
            white_list=[
                message.from_id,
                *[
                    item.member_id
                    for item in (await message.api.messages.get_conversation_members(peer_id=message.peer_id)).items
                    if item.is_admin and item.member_id > 0
                ]
            ],
            warn_message=warn_text,
            time=delay_time
        ))
        await edit_message(
            message,
            f"✅ Слоумо режим в этой беседе установлен:\n"
            f"⏱ Задержка {delay_time} сек.\n"
            f"⚠ Текст предупреждения: {warn_text}"
        )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -слоумо")
@logger_decorator
async def disable_sloumo_wrapper(
        message: Message,
        **kwargs
):
    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i
    if index is not None:
        db.sloumo.pop(index)
    db.save()
    await edit_message(
        message,
        f"✅ Слоумо режим в этой беседе был отключен\n"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> слоумо")
@logger_decorator
async def show_sloumo_wrapper(
        message: Message,
        **kwargs
):
    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i
    if index is None:
        await edit_message(message, 'Слоумо режим в этой беседе не настроен')
        return

    white_list = ""
    users = (await message.api.users.get(user_ids=db.sloumo[index].white_list))
    for _user in users:
        white_list += f"[id{_user.id}|{_user.first_name} {_user.last_name}]\n"

    await edit_message(
        message,
        f"✅ Слоумо режим в этой беседе установлен:\n"
        f"⏱ Задержка {db.sloumo[index].time} сек.\n"
        f"⚠ Текст предупреждения: {db.sloumo[index].warn_message}\n"
        f"Белый список: {white_list}"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> слоумо +белый список [id<user_id:int>|<foo>")
@logger_decorator
async def show_sloumo_wrapper(
        message: Message,
        user_id: int,
        **kwargs
):
    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i
    if index is None:
        await edit_message(message, 'Слоумо режим в этой беседе не настроен')
        return

    db.sloumo[index].white_list.append(user_id)
    db.save()
    white_list = ""
    users = (await message.api.users.get(user_ids=db.sloumo[index].white_list))
    for _user in users:
        white_list += f"[id{_user.id}|{_user.first_name} {_user.last_name}]\n"

    await edit_message(
        message,
        f"✅ Пользователь добавлен в белый список\n"
        f"Белый список: {white_list}"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> слоумо -белый список [id<user_id:int>|<foo>")
@logger_decorator
async def show_sloumo_wrapper(
        message: Message,
        user_id: int,
        **kwargs
):
    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i
    if index is None:
        await edit_message(message, 'Слоумо режим в этой беседе не настроен')
        return

    if user_id in db.sloumo[index].white_list:
        db.sloumo[index].white_list.remove(user_id)
        db.save()
    white_list = ""
    users = (await message.api.users.get(user_ids=db.sloumo[index].white_list))
    for _user in users:
        white_list += f"[id{_user.id}|{_user.first_name} {_user.last_name}]\n"

    await edit_message(
        message,
        f"✅ Пользователь удален из белого списка\n"
        f"Белый список: {white_list}"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> слоумо время <delay_time:int>")
@logger_decorator
async def show_sloumo_wrapper(
        message: Message,
        delay_time: int,
        **kwargs
):
    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i
    if index is None:
        await edit_message(message, 'Слоумо режим в этой беседе не настроен')
        return
    db.sloumo[index].time = delay_time
    db.save()
    await edit_message(
        message,
        f"✅ Время слоумо режима изменено на {delay_time}"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> слоумо текст <text>")
@logger_decorator
async def show_sloumo_wrapper(
        message: Message,
        text: str,
        **kwargs
):
    db = Database.get_current()
    index = None
    for i in range(len(db.sloumo)):
        if db.sloumo[i].chat_id == message.chat_id:
            index = i
    if index is None:
        await edit_message(message, 'Слоумо режим в этой беседе не настроен')
        return
    db.sloumo[index].warn_message = text
    db.save()
    await edit_message(
        message,
        f"✅ Текст предупреждени я изменен на \"{text}\""
    )
