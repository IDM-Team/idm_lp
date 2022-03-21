import argparse
import asyncio
import datetime
import json
import os
import traceback

import requests
import vkbottle.api
from vkbottle.api import UserApi
from vkbottle.user import User

from idm_lp import const, timers
from idm_lp.commands import commands_bp
from idm_lp.database import Database, DatabaseError
from idm_lp.error_handlers import error_handlers_bp
from idm_lp.idm_api import IDMAPI, IDMException
from idm_lp.logger import logger, Logger, LoggerLevel
from idm_lp.utils import SemVer

parser = argparse.ArgumentParser(
    description='LP модуль позволяет работать приемнику сигналов «IDM multi» работать в любых чатах.\n'
                'Так же он добавляет игнор, глоигнор, мут и алиасы.'
)

parser.add_argument(
    '--config_path',
    type=str,
    dest="config_path",
    default="config.json",
    help='Путь до файла с конфингом'
)

parser.add_argument(
    '--base_domain',
    type=str,
    dest="base_domain",
    default="https://idmduty.ru",
    help='Базовый домен'
)

parser.add_argument(
    '--use_app_data',
    dest="use_app_data",
    action="store_const",
    const=True,
    help='Использовать папку AppData/IDM (Windows).\n'
         'При использовании этой настройки AppData/IDM и config_path складываются'
)

parser.add_argument(
    '--logger_level',
    dest="logger_level",
    type=str,
    default="INFO",
    help='Уровень логирования.'
)
parser.add_argument(
    '--log_to_path',
    dest="log_to_path",
    action="store_const",
    const=True,
    help='Логи в файл'
)

parser.add_argument(
    '--enable_eval',
    dest="enable_eval",
    action="store_const",
    const=True,
    help='Разрешить eval/exec'
)
parser.add_argument(
    '--use_local_db',
    dest="use_local_db",
    action="store_const",
    const=True,
    help='Не использовать ДБ IDM'
)


@Database.add_on_save
async def clear_timers(db: Database):
    now = datetime.datetime.now()
    timers_copy = db.timers[:]
    for timer in timers_copy:
        if timer.type == timer.type.DATE:
            if timer.run_date < now:
                db.timers.remove(timer)


@Database.add_on_save
async def on_db_save(db: Database):
    api = vkbottle.api.API(tokens=db.tokens)
    const.scheduler.pause()

    timers_ids = [x.id for x in const.scheduler.get_jobs()]
    if db.auto_infection:
        if 'auto_infection_timer' not in timers_ids:
            const.scheduler.add_job(
                timers.auto_infection_timer,
                id='auto_infection_timer',
                name='Таймер на авто заражение',
                args=(api, db,),
                trigger='interval',
                seconds=db.auto_infection_interval,
                max_instances=1
            )
            await timers.auto_infection_timer(api, db)
    else:
        if 'auto_infection_timer' in timers_ids:
            const.scheduler.remove_job('auto_infection_timer')
    for timer in db.timers:
        if timer.method == timer.method.SEND_MESSAGE:
            if timer.id not in timers_ids:
                const.scheduler.add_job(
                    timers.send_message_timer,
                    **timer.scheduler_params,
                    max_instances=1,
                    args=(api, db, timer,)
                )
    db_timers_ids = ['auto_infection_timer', *[x.id.hex for x in db.timers]]
    for job in const.scheduler.get_jobs():
        if job.id not in db_timers_ids:
            const.scheduler.remove_job(job.id)
    const.scheduler.resume()


@Database.add_on_save
async def on_db_save_to_server(db: Database):
    if not const.USE_LOCAL_DB:
        await IDMAPI.get_current().save_lp_info(db.tokens[0], db.get_to_server())
        logger.info("Конфиг отправлен на сервер")


async def lp_startup():
    api = UserApi.get_current()
    text = (
        f'[IDM LP]\n'
        f'❤ Запущена версия IDM LP {const.__version__}\n'
    )
    version_rest = requests.get(const.VERSION_REST).json()

    last_stable = SemVer(version_rest['version'])
    current = SemVer(const.__version__)

    if current < last_stable:
        text += (
            f"\n💬 Доступно обновление {version_rest['version']}\n"
            f"{version_rest['description']}"
        )
        if 'DYNO' in os.environ:
            text += (
                "\n\nЧтобы обновить введите !с обновитьлп"
            )

    elif current > last_stable:
        text += "\n💬 Обратите внимание! Вы используете экспериментальную не стабильную версию."

    const.__author__ = version_rest['author']

    await api.messages.send(
        peer_id=await api.user_id,
        random_id=0,
        message=text
    )

    try:
        await IDMAPI.get_current().ping()
    except IDMException as ex:
        await api.messages.send(
            random_id=0,
            peer_id=await api.user_id,
            message=f"[IDM LP]\n⚠ Произошла ошибка при проверке подлинности секретного кода:\n💬 {ex}"
        )
        raise KeyboardInterrupt()


def run_lp():
    args = parser.parse_args()

    const.CONFIG_PATH = args.config_path
    const.BASE_DOMAIN = args.base_domain
    const.USE_APP_DATA = args.use_app_data if args.use_app_data else False
    const.LOG_TO_PATH = args.log_to_path if args.log_to_path else False
    const.LOGGER_LEVEL = args.logger_level
    const.ENABLE_EVAL = args.enable_eval if args.enable_eval else False
    const.USE_LOCAL_DB = args.use_local_db if args.use_local_db else False

    if isinstance(logger, Logger):
        logger.global_logger_level = LoggerLevel.get_int(const.LOGGER_LEVEL)

    logger.warning(
        f"\n\nЗапуск с параметрами:\n"
        f" -> Уровень логирования              -> {const.LOGGER_LEVEL}\n"
        f" -> Логи в файл                       -> {const.LOG_TO_PATH}\n"
        f" -> Путь до файла с конфигурацией     -> {Database.get_path()}\n"
        f" -> Использовать папку AppData/IDM    -> {const.USE_APP_DATA}\n"
        f" -> Базовый домен                     -> {const.BASE_DOMAIN}\n"
        f" -> Использовать локальную БД         -> {const.USE_LOCAL_DB}\n"
        f" -> Разрешить eval/exec               -> {const.ENABLE_EVAL}\n\n"
    )

    idm_api = IDMAPI(const.BASE_DOMAIN, const.APP_USER_AGENT)
    IDMAPI.set_current(idm_api)

    try:
        db = Database.load()
        if not const.USE_LOCAL_DB:
            db = db.load_from_server()
        Database.set_current(db)
    except DatabaseError as ex:
        logger.error(
            f"{ex.name} | {ex.description}"
        )
        exit(-1)
    except json.JSONDecodeError as ex:
        logger.error(
            f'При запуске произошла ошибка базы данных.\n'
            f'Проверьте целостность данных.\n'
            f'Строка: {ex.lineno}, столбец: {ex.colno}.'
        )
        exit(-1)
    except IDMException as ex:
        logger.error(str(ex))
        exit(-1)
    except Exception as ex:
        logger.error(f'При запуске произошла ошибка [{ex.__class__.__name__}] {ex}\n{traceback.format_exc()}')
        exit(-1)
    else:
        from idm_lp.validators import (
            alias,
            role_play_command,
            self_prefix,
            duty_prefix,
            service_prefix,
            repeater_word,
            yes_or_no
        )

        user = User(
            tokens=db.tokens,
            debug=const.LOGGER_LEVEL,
            log_to_path=const.LOG_TO_PATH
        )
        user.set_blueprints(
            *commands_bp,
            *error_handlers_bp,
        )
        const.scheduler.start()
        user.run_polling(
            auto_reload=False,
            on_startup=lp_startup,
        )
