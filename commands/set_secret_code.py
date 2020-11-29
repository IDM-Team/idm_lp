from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='set_secret_code_blueprint'
)


@user.on.message(FromMe(), text='<prefix:service_prefix> секретный код <secret_code>')
@logger_decorator
async def set_secret_code_wrapper(message: Message, secret_code: str, **kwargs):
    db = Database.get_current()
    db.secret_code = secret_code
    db.save()
    await edit_message(
        message,
        "✅ Секретный код установлен"
    )
