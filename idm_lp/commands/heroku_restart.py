import os

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.utils import edit_message

user = Blueprint(
    name='heroku_restart_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> heroku restart")
async def heroku_restart_wrapper(message: Message, **kwargs):
    if 'DYNO' in os.environ:
        await edit_message(message, "✅ IDM LP будет перезапущен и обновлен!")
        exit(0)
    await edit_message(message, "⚠ Окружение Heroku не было найдено")
