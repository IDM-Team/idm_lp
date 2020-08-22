import argparse
import sys
import traceback

import requests
from vkbottle.api import UserApi
from vkbottle.user import User

import const
from commands import commands_bp
from error_handlers import error_handlers_bp
from objects import Database
from objects.json_orm import DatabaseError

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


async def lp_startup():
    api = UserApi.get_current()
    text = f'IDM multi LP запущен\n' \
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


if __name__ == '__main__':
    args = parser.parse_args()

    const.CONFIG_PATH = args.config_path
    const.USE_APP_DATA = args.use_app_data if args.use_app_data else False

    sys.stdout.write(
        f"Запуск с параметрами:\n"
        f" -> Уровень логгирования              -> {args.logger_level}\n"
        f" -> Путь до файла с конфингом         -> {const.CONFIG_PATH}\n"
        f" -> Использовать папку AppData/IDM    -> {const.USE_APP_DATA}\n"
    )

    try:
        db = Database.load(is_startup=True)
    except DatabaseError as ex:
        exit(-1)
    except Exception as ex:
        sys.stdout.write(f'При запуске произошла ошибка [{ex.__class__.__name__}] {ex}\n{traceback.format_exc()}')
        exit(-1)
    else:
        from validators import *

        user = User(
            tokens=db.tokens,
            debug=args.logger_level
        )
        user.set_blueprints(
            *commands_bp,
            *error_handlers_bp
        )
        user.run_polling(
            auto_reload=False,
            on_startup=lp_startup
        )
        sys.stdout.write(f'Пуллинг запущен\n')
