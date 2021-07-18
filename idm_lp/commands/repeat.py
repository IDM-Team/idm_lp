from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.rules import TrustedRule
from idm_lp.utils import edit_message

user = Blueprint(
    name='repeat_blueprint'
)


@user.on.message_handler(TrustedRule(), text='<signal:repeater_word>')
@logger_decorator
async def repeat_wrapper(message: Message, signal: str, **kwargs):
    db = Database.get_current()
    if not db.repeater_active:
        return
    return signal


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> +повторялка')
@logger_decorator
async def repeat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.repeater_active = True
    db.save()
    await edit_message(message, "✅ Повторялка включена")


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> -повторялка')
@logger_decorator
async def repeat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.repeater_active = False
    db.save()
    await edit_message(message, "✅ Повторялка выключена")


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> повторялка <text>')
@logger_decorator
async def repeat_wrapper(message: Message, text: str, **kwargs):
    db = Database.get_current()
    db.repeater_word = text
    db.save()
    await edit_message(message, f"✅ Префикс повторялки установлен на <<{text}>>")
