import json
import re

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.database import Alias
from idm_lp.idm_api import IDMAPI, IDMException
from idm_lp.logger import logger_decorator

user = Blueprint(
    name='aliases_blueprint'
)


async def send_signal(
        message: Message,
        message_text: str
):
    try:
        await IDMAPI.get_current().send_my_signal(
            from_id=message.from_id, peer_id=message.peer_id,
            conversation_message_id=message.conversation_message_id,
            date=message.date, text=message_text, vk_message=json.loads(message.json())
        )
    except IDMException as ex:
        await message.api.messages.send(
            random_id=0,
            peer_id=await message.api.user_id,
            message=f"[IDM LP]\n⚠ Произошла ошибка при отправке сигнала на сервер IDM:\n💬 {ex}"
        )


@user.on.message_handler(FromMe(), text=['<alias:alias> <signal>', '<alias:alias>', '<alias:alias>\n<signal>'])
@logger_decorator
async def duty_signal(message: Message, alias: Alias, **kwargs):
    await send_signal(
        message,
        re.compile(alias.regexp, re.IGNORECASE).sub(
            f".с {alias.command_to}", message.text
        )
    )
