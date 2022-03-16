import json

from vkbottle.user import Blueprint, Message

from idm_lp.idm_api import IDMAPI, IDMException
from idm_lp.logger import logger_decorator

user = Blueprint(
    name='duty_signal_blueprint'
)


# noinspection DuplicatedCode
async def send_signal(
        message: Message,
        prefix: str,
        signal: str
):
    try:
        await IDMAPI.get_current().send_signal(
            from_id=message.from_id, peer_id=message.peer_id,
            conversation_message_id=message.conversation_message_id,
            date=message.date, text=prefix + ' ' + signal, vk_message=json.loads(message.json())
        )
    except IDMException as ex:
        await message.api.messages.send(
            random_id=0,
            peer_id=await message.api.user_id,
            message=f"[IDM LP]\n⚠ Произошла ошибка при отправке сигнала на сервер IDM:\n💬 {ex}"
        )


@user.on.message_handler(text='<prefix:duty_prefix> [id<user_id:int>|<name>] <signal>')
@logger_decorator
async def duty_signal(message: Message, prefix: str, user_id: int, signal: str, **kwargs):
    if user_id != await message.api.user_id:
        return
    await send_signal(message, prefix, signal)


@user.on.message_handler(text='<prefix:duty_prefix> <signal>')
@logger_decorator
async def duty_signal(message: Message, prefix: str, signal: str, **kwargs):
    user_ids = []
    if message.reply_message:
        user_ids.append(message.reply_message.from_id)
    for fwd in message.fwd_messages:
        user_ids.append(fwd.from_id)

    if await message.api.user_id not in user_ids:
        return

    await send_signal(message, prefix, signal)
