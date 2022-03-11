from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp import const
from idm_lp.database import Database
from idm_lp.logger import logger_decorator
from idm_lp.utils import edit_message

user = Blueprint(
    name='auto_infection_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +автозаражение")
@logger_decorator
async def activate_auto_infection_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.auto_infection = True
    db.save(True)
    await edit_message(
        message,
        "✅ Автоматическое заражение включено"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -автозаражение")
@logger_decorator
async def deactivate_auto_infection_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.auto_infection = False
    db.save(True)
    await edit_message(
        message,
        "✅ Автоматическое заражение выключено"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автозаражение интервал <int:interval>")
@logger_decorator
async def set_auto_infection_interval_wrapper(message: Message, interval: int, **kwargs):
    db = Database.get_current()
    if interval < 120:
        await edit_message(
            message,
            "⚠ Интервал автоматического заражения не может быть меньше 2х минут"
        )
        return

    db.auto_infection_interval = interval
    db.save(True)
    await edit_message(
        message,
        f"✅ Интервал автоматического заражения установлен на {interval} сек."
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автозаражение аргумент <argument>")
@logger_decorator
async def set_auto_infection_argument_wrapper(message: Message, argument: str, **kwargs):
    db = Database.get_current()
    db.auto_infection_argument = argument
    db.save(True)
    await edit_message(
        message,
        "✅ Аргумент автоматического заражения изменен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автозаражение установить чат")
@logger_decorator
async def set_auto_infection_chat_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.auto_infection_peer_id = message.peer_id
    db.save(True)
    await edit_message(
        message,
        "✅ Чат автоматического заражения изменен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> автозаражение")
@logger_decorator
async def show_auto_infection_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    jobs = const.scheduler.get_jobs()
    next_run_time = None
    for job in jobs:
        if job.id == 'auto_infection_timer':
            next_run_time = job.next_run_time
    text = (
        f"☢ Состояние автоматического заражения:\n"
        f"{'Запущен' if db.auto_infection else 'Остановлен'}\n"
        f"⏱ Интервал заражения: {db.auto_infection_interval} сек.\n"
        f"🧨 Аргумент заражения: {db.auto_infection_argument}\n"
        f"💬 Чат заражения: {db.auto_infection_peer_id}\n\n"
    )
    if next_run_time:
        text += f'⏳ Следующий запуск: {next_run_time.strftime("%Y-%m-%d %H:%M:%S")}'
    await edit_message(message, text)
