import time

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message
from utils import edit_message

user = Blueprint(
    name='ping_blueprint'
)


async def get_ping(message: Message, answer: str) -> str:
    delta = round(time.time() - message.date, 2)

    # А ты думал тут все чесно будет? Не, я так не работаю...
    if delta < 0:
        delta = 0.0000000001

    return f"{answer} Модуль ЛП\n" \
           f"Ответ через {delta} с"


@user.on.message(FromMe(), text="<prefix:service_prefix> пинг")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> пинг")
async def ping_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "ПОНГ")
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> пиу")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> пиу")
async def ping_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "ПАУ")
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> кинг")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> кинг")
async def ping_wrapper(message: Message, **kwargs):
    await edit_message(
        message,
        await get_ping(message, "КОНГ")
    )
