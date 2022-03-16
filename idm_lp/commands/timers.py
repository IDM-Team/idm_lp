import datetime
import typing

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp import const
from idm_lp.database import Database, Timer, TimerMethod, TimerType
from idm_lp.logger import logger_decorator
from idm_lp.utils import edit_message, parse_cron_text

user = Blueprint(
    name='timers_blueprint'
)


class E(Exception):
    def __init__(self, m: str): self.m = m

    def __str__(self): return self.m


def get_arguments(m: str, mode: TimerType) -> typing.Tuple[
    typing.Any,
    typing.Optional[str]
]:
    data = m.split('\n')
    if len(data) < 2:
        raise E("⚠ Необходимо указать дату и сообщение")
    try:
        data, text = data[0], '\n'.join(data[1:])
    except IndexError:
        data = data[0]
        text = None
    if mode == TimerType.INTERVAL:
        try:
            return int(data), text
        except ValueError:
            raise E("⚠ Интервал должен быть числом")
    elif mode == TimerType.CRON:
        try:
            parse_cron_text(data)
            return data, text
        except ValueError:
            raise E("⚠ Не верное CRON выражение.")
    else:
        try:
            return datetime.datetime.strptime(data, '%Y.%m.%d %H:%M:%S'), text
        except ValueError:
            raise E("⚠ Дата должна быть в формате 2022.03.16 12:46:22")


def check_name(db: Database, name: str):
    if name.lower() in db.timers:
        raise E("⚠ Такой таймер уже существует")


async def create_timer(message: Message, name, text_message, timer_type: TimerType):
    with Database.get_current() as db:
        try:
            check_name(db, name)
            date, msg_text = get_arguments(text_message, timer_type)
            attachment = ",".join([
                f"{attachment['type']}"
                f"{attachment[attachment['type']]['owner_id']}_"
                f"{attachment[attachment['type']]['id']}"
                for attachment in message.attachments
            ])
            if not msg_text and not attachment:
                raise E("⚠ Необходим текст сообщения ")
            db.timers.append(
                Timer(
                    name=name,
                    type=timer_type,
                    method=TimerMethod.SEND_MESSAGE,
                    peer_id=message.peer_id,
                    message_text=msg_text,
                    message_attachment=attachment,
                    run_date=date if timer_type == TimerType.DATE else None,
                    interval=date if timer_type == TimerType.INTERVAL else None,
                    cron=date if timer_type == TimerType.CRON else None
                )
            )
            await edit_message(
                message,
                "✅ Таймер успешно создан"
            )
        except E as ex:
            await edit_message(
                message,
                str(ex)
            )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> таймеры")
@logger_decorator
async def show_timers_wrapper(
        message: Message,
        **kwargs
):
    db = Database.get_current()
    text = "📃 Ваши таймеры:\n"
    for index, timer in enumerate(db.timers, 1):
        text += f"{index}. {timer.name}\n"
    await edit_message(
        message,
        text
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> !таймеры")
@logger_decorator
async def show_timers_from_scheduler_wrapper(
        message: Message,
        **kwargs
):
    text = "📃 Ваши таймеры (из планировщика):\n"
    for index, job in enumerate(const.scheduler.get_jobs(), 1):
        text += f"{index}. {job.name} {job.next_run_time.strftime('%Y.%m.%d %H:%M:%S')}\n"
    await edit_message(
        message,
        text
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +таймер <name> смс <text_message>")
@logger_decorator
async def add_date_timer_wrapper(
        message: Message,
        name: str,
        text_message: str,
        **kwargs
):
    await create_timer(message, name, text_message, TimerType.DATE)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +цтаймер <name> смс <text_message>")
@logger_decorator
async def add_interval_timer_wrapper(
        message: Message,
        name: str,
        text_message: str,
        **kwargs
):
    await create_timer(message, name, text_message, TimerType.INTERVAL)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +ктаймер <name> смс <text_message>")
@logger_decorator
async def add_cron_timer_wrapper(
        message: Message,
        name: str,
        text_message: str,
        **kwargs
):
    await create_timer(message, name, text_message, TimerType.CRON)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -таймер <name>")
@logger_decorator
async def remove_timer_wrapper(
        message: Message,
        name: str,
        **kwargs
):
    with Database.get_current() as db:
        timer = None
        for tim in db.timers:
            if tim.name.lower() == name.lower():
                timer = tim
                break
        if not timer:
            await edit_message(
                message,
                "⚠ Таймер не найден"
            )
            return
        db.timers.remove(timer)
        await edit_message(
            message,
            f"⚠ Таймер <<{name}>> успешно удален"
        )
