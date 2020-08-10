import sys

import requests
from vkbottle.user import Blueprint, Message

from objects import Database

user = Blueprint(
    name='duty_signal_blueprint'
)


@user.on.message(text='<prefix:duty_prefix> [id<user_id:int>|<name>] <signal>')
@user.on.chat_message(text='<prefix:duty_prefix> [id<user_id:int>|<name>] <signal>')
async def duty_signal(message: Message, prefix: str, user_id: int, signal: str, **kwargs):
    sys.stdout.write(f"Сигнал дежурному: {signal}\n")
    dp = Database.load()
    if user_id != await message.api.user_id:
        return
    message_ = await message.get()
    __model = {
        "user_id": await message.api.user_id,
        "method": "lpSendSignal",
        "secret": dp.secret_code,
        "message": {
            "conversation_message_id": message_['conversation_message_id'],
            "from_id": message_['from_id'],
            "date": message.date,
            "text": prefix + ' ' + signal,
            "peer_id": message.peer_id
        },
        "object": {
            "chat": None,
            "from_id": message_['from_id'],
            "value": prefix + ' ' + signal,
            "conversation_message_id": message_['conversation_message_id']
        },
        "vkmessage": message_
    }
    requests.post(
        'https://irisduty.ru/callback/',
        json=__model
    )
