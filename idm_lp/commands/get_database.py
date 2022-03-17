from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.database import Database
from idm_lp.idm_api import IDMAPI
from idm_lp.logger import logger_decorator
from idm_lp.utils import edit_message

user = Blueprint(
    name='set_db_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> получить бд")
@logger_decorator
async def set_db_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    try:
        new_db = db.load_from_server()
    except Exception as ex:
        await edit_message(
            message,
            f"⚠ Ошибка: {ex}"
        )
        return
    new_db.save()
    Database.set_current(new_db)
    await edit_message(
        message,
        "✅ Конфигурация успешно обновлена с сервера"
    )
