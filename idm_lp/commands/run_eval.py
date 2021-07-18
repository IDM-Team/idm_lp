import traceback

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp import const
from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.utils import edit_message

user = Blueprint(
    name='run_eval_blueprint'
)


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> eval <signal>')
@logger_decorator
async def eval_signal_wrapper(message: Message, signal: str, **kwargs):
    if not const.ENABLE_EVAL:
        return
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


@user.on.message_handler(FromMe(), text='<prefix:service_prefix> exec <signal>', lower=True)
@logger_decorator
async def exec_signal_wrapper(message: Message, signal: str, **kwargs):
    if not const.ENABLE_EVAL:
        return
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
