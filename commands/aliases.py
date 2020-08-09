import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from objects import Database, Alias

user = Blueprint(
    name='aliases_blueprint'
)


@user.on.message(FromMe(), text=['<alias:alias> <signal>', '<alias:alias>'])
@user.on.chat_message(FromMe(), text=['<alias:alias> <signal>', '<alias:alias>'])
async def duty_signal(message: Message, alias: Alias, signal: str = None):
    message_ = await message.get()
    db = Database.load()

    prepared_text = db.self_prefixes[0] + ' ' + alias.command_to
    prepared_text += f" {signal}" if signal else ''

    __model = {
        "user_id": message_['from_id'],
        "method": "lpSendMySignal",
        "secret": db.secret_code,
        "message": {
            "conversation_message_id": message_['conversation_message_id'],
            "from_id": message_['from_id'],
            "date": message.date,
            "text": prepared_text,
            "peer_id": message.peer_id
        },
        "object": {
            "chat": None,
            "from_id": message_['from_id'],
            "value": prepared_text,
            "conversation_message_id": message_['conversation_message_id']
        },
        "vkmessage": message_
    }

    requests.post(
        'https://irisduty.ru/callback/',
        json=__model
    )
