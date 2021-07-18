from typing import Optional

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database, Alias
from idm_lp.utils import send_request

user = Blueprint(
    name='aliases_blueprint'
)


async def send_signal(
        database: Database,
        message: Message,
        alias: Alias,
        separator: str = ' ',
        signal: Optional[str] = None
):
    message_ = message.dict()
    prepared_text = database.self_prefixes[0] + ' ' + alias.command_to
    prepared_text += f"{separator}{signal}" if signal else ''

    __model = {
        "user_id": message_['from_id'],
        "method": "lpSendMySignal",
        "secret": database.secret_code,
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

    await send_request(__model)


@user.on.message_handler(FromMe(), text=['<alias:alias> <signal>', '<alias:alias>'])
@logger_decorator
async def duty_signal(message: Message, alias: Alias, signal: str = None):
    db = Database.get_current()
    await send_signal(db, message, alias, ' ', signal)


@user.on.message_handler(FromMe(), text='<alias:alias>\n<signal>')
@logger_decorator
async def duty_signal_new_line(message: Message, alias: Alias, signal: str):
    db = Database.get_current()
    await send_signal(db, message, alias, '\n', signal)
