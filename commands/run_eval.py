import traceback

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from logger import logger_decorator
from objects import Database
from utils import edit_message

user = Blueprint(
    name='run_eval_blueprint'
)


@user.on.message(FromMe(), text='<prefix:service_prefix> eval <signal>')
@user.on.chat_message(FromMe(), text='<prefix:service_prefix> eval <signal>')
@logger_decorator
async def eval_signal_wrapper(message: Message, signal: str, **kwargs):
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


@user.on.message(FromMe(), text='<prefix:service_prefix> exec <signal>')
@user.on.chat_message(FromMe(), text='<prefix:service_prefix> exec <signal>')
@logger_decorator
async def exec_signal_wrapper(message: Message, signal: str, **kwargs):
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
