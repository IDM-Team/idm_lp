from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

user = Blueprint(
    name='ping_blueprint'
)


@user.on.message(FromMe(), text="<prefix:service_prefix> пинг")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> пинг")
async def ping_wrapper(message: Message):
    await message("ПОНГ")


@user.on.message(FromMe(), text="<prefix:service_prefix> пиу")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> пиу")
async def ping_wrapper(message: Message):
    await message("ПАУ")


@user.on.message(FromMe(), text="<prefix:service_prefix> кинг")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> кинг")
async def ping_wrapper(message: Message):
    await message("КОНГ")
