from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.utils import send_request

user = Blueprint(
    name='self_signal_blueprint'
)


@user.on.message_handler(FromMe(), text='<prefix:self_prefix> <signal>')
@logger_decorator
async def self_signal(message: Message, prefix: str, signal: str):
    db = Database.get_current()
    message_ = message.dict()
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

    await send_request(__model)
