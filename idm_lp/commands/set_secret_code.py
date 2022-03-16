from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.utils import edit_message

user = Blueprint(
    name='set_secret_code_blueprint'
)


@user.on.message(FromMe(), text='<prefix:service_prefix> секретный код <secret_code>')
@logger_decorator
async def set_secret_code_wrapper(message: Message, secret_code: str, **kwargs):
    with Database.get_current() as db:
        db.secret_code = secret_code
    await edit_message(
        message,
        "✅ Секретный код установлен"
    )


@user.on.message(FromMe(), text='<prefix:service_prefix> токен каптчи <secret_code>')
@logger_decorator
async def set_secret_code_wrapper(message: Message, ru_captcha_key: str, **kwargs):
    with Database.get_current() as db:
        db.ru_captcha_key = ru_captcha_key
    await edit_message(
        message,
        "✅ Токен каптчи установлен"
    )
