import traceback

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message
from vkbottle.utils import logger

from objects import Database
from utils import edit_message

user = Blueprint(
    name='duty_signal_blueprint'
)


@user.on.message(FromMe(), text='<prefix:duty_prefix> eval <signal>')
@user.on.chat_message(FromMe(), text='<prefix:duty_prefix> eval <signal>')
async def eval_signal_wrapper(message: Message, signal: str, **kwargs):
    logger.info(f'eval -> {signal}')
    db = Database.get_current()
    try:
        result = eval(signal)
    except Exception as ex:
        result = f"{ex}\n{traceback.format_exc()}"

    if not result:
        result = '✅ Выполнено'

    await edit_message(
        message,
        result
    )


@user.on.message(FromMe(), text='<prefix:duty_prefix> exec <signal>')
@user.on.chat_message(FromMe(), text='<prefix:duty_prefix> exec <signal>')
async def exec_signal_wrapper(message: Message, signal: str, **kwargs):
    logger.info(f'exec -> {signal}')
    db = Database.get_current()
    try:
        result = exec(signal)
    except Exception as ex:
        result = f"{ex}\n{traceback.format_exc()}"

    if not result:
        result = '✅ Выполнено'

    await edit_message(
        message,
        result
    )
