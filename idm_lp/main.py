import argparse
import json
import traceback

import aiohttp
import requests
import vkbottle.api
from vkbottle.api import UserApi
from vkbottle.user import User

from idm_lp import const, timers
from idm_lp.commands import commands_bp
from idm_lp.database import Database, DatabaseError
from idm_lp.error_handlers import error_handlers_bp
from idm_lp.logger import logger, Logger, LoggerLevel
from idm_lp.utils import check_ping

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
    help='Уровень логгирования.'
)

parser.add_argument(
    '--vkbottle_logger_level',
    dest="vkbottle_logger_level",
    type=str,
    default="ERROR",
    help='Уровень логгирования VKBottle.'
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


@Database.add_on_save
async def on_db_save(db: Database):
    api = vkbottle.api.API(tokens=db.tokens)
    const.scheduler.pause()
    const.scheduler.remove_all_jobs()
    if db.auto_infection:
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
    const.scheduler.resume()


@Database.add_on_save
async def on_db_save_to_server(db: Database):
    async with aiohttp.ClientSession(headers={"User-Agent": const.APP_USER_AGENT}) as session:
        async with session.post(
                const.SAVE_LP_INFO_LINK(),
                json={'access_token': db.tokens[0], 'config': json.loads(db.json())}
        ) as resp:
            l = await resp.json()
            s = 1


def lp_startup():
    async def _lp_startup():
        api = UserApi.get_current()
        database = Database.get_current()
        await on_db_save(database)
        text = f'IDM LP запущен\n' \
               f'Текущая версия: v{const.__version__}'
        version_rest = requests.get(const.VERSION_REST).json()

        if version_rest['version'] != const.__version__:
            text += f"\n\n Доступно обновление {version_rest['version']}\n" \
                    f"{version_rest['description']}\n" \
                    f"{const.GITHUB_LINK}"

        await api.messages.send(
            peer_id=await api.user_id,
            random_id=0,
            message=text
        )

        async with aiohttp.ClientSession(headers={"User-Agent": const.APP_USER_AGENT}) as session:
            async with session.post(const.GET_LP_INFO_LINK(), json={'access_token': database.tokens[0]}) as resp:
                response = await resp.json()
                if 'error' in response:
                    await api.messages.send(
                        peer_id=await api.user_id,
                        random_id=0,
                        message=f"⚠ Ошибка: {response['error']['detail']}"
                    )
                    raise KeyboardInterrupt()
                else:
                    if not response['response']['is_active']:
                        await api.messages.send(
                            peer_id=await api.user_id,
                            random_id=0,
                            message=f"⚠ Ошибка: дежурный не активен"
                        )
                        raise KeyboardInterrupt()
                    database = Database.parse_obj(response['response']['config'])
                    Database.set_current(database)
                    database.save(True)

        await check_ping(database.secret_code)

    return _lp_startup


def run_lp():
    args = parser.parse_args()

    const.CONFIG_PATH = args.config_path
    const.BASE_DOMAIN = args.base_domain
    const.USE_APP_DATA = args.use_app_data if args.use_app_data else False
    const.LOG_TO_PATH = args.log_to_path if args.log_to_path else False
    const.LOGGER_LEVEL = args.logger_level
    const.VKBOTTLE_LOGGER_LEVEL = args.vkbottle_logger_level
    const.ENABLE_EVAL = args.enable_eval if args.enable_eval else False

    if isinstance(logger, Logger):
        logger.global_logger_level = LoggerLevel.get_int(const.LOGGER_LEVEL)

    logger.warning(
        f"\n\nЗапуск с параметрами:\n"
        f" -> Уровень логгирования              -> {const.LOGGER_LEVEL}\n"
        f" -> Уровень логгирования VKBottle     -> {const.VKBOTTLE_LOGGER_LEVEL}\n"
        f" -> Логи в файл                       -> {const.LOG_TO_PATH}\n"
        f" -> Путь до файла с конфингом         -> {Database.get_path()}\n"
        f" -> Использовать папку AppData/IDM    -> {const.USE_APP_DATA}\n"
        f" -> Базовый домен                     -> {const.BASE_DOMAIN}\n"
        f" -> API                               -> {const.GET_LP_INFO_LINK()}\n"
        f" -> Callback link                     -> {const.CALLBACK_LINK()}\n"
        f" -> Разрешить eval/exec               -> {const.ENABLE_EVAL}\n\n"
    )

    try:
        db = Database.load()
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
            debug=const.VKBOTTLE_LOGGER_LEVEL,
            log_to_path=const.LOG_TO_PATH
        )
        user.set_blueprints(
            *commands_bp,
            *error_handlers_bp,
        )
        const.scheduler.start()

        user.run_polling(
            auto_reload=False,
            on_startup=lp_startup(),
        )
