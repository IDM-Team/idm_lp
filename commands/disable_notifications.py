from vkbottle.rule import ChatActionRule, FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='disable_notifications_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> выключать уведы")
@logger_decorator
async def allow_disable_notifications_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.disable_notifications = True
    db.save()
    await edit_message(message, "&#9989; Настройка изменена")


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> не выключать уведы")
@logger_decorator
async def deny_disable_notifications_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.disable_notifications = False
    db.save()
    await edit_message(message, "&#9989; Настройка изменена")

