import json

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.idm_api import IDMAPI, IDMException
from idm_lp.logger import logger_decorator

user = Blueprint(
    name='self_signal_blueprint'
)


@user.on.message_handler(FromMe(), text='<prefix:self_prefix> <signal>')
@logger_decorator
async def self_signal(message: Message, prefix: str, signal: str):
    try:
        await IDMAPI.get_current().send_my_signal(
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
