import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from objects import Database

user = Blueprint(
    name='self_signal_blueprint'
)


@user.on.message(FromMe(), text='<prefix:self_prefix> <signal>')
@user.on.chat_message(FromMe(), text='<prefix:self_prefix> <signal>')
async def self_signal(message: Message, prefix: str, signal: str):
    message_ = await message.get()
    db = Database.load()
    __model = {
        "user_id": message_['from_id'],
        "method": "lpSendMySignal",
        "secret": db.secret_code,
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
