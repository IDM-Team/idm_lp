from const import __version__, __author__
from vkbottle.user import User
from vkbottle.api import UserApi
from objects import Database
from loguru import logger
from commands import commands_bp


async def lp_startup():
    api = UserApi.get_current()
    await api.messages.send(
        peer_id=await api.user_id,
        random_id=0,
        message=f'IDM multi LP v{__version__} запущен'
    )


async def lp_shutdown():
    api = UserApi.get_current()
    await api.messages.send(
        peer_id=await api.user_id,
        random_id=0,
        message=f'IDM multi LP v{__version__} остановлен'
    )


if __name__ == '__main__':
    logger.info(f'Запускаю IDM multi LP by {__author__} v{__version__}')
    try:
        db = Database.load()
    except Database.DatabaseError as ex:
        logger.exception(ex)
        exit(-1)
    except Exception as ex:
        logger.exception(ex)
        exit(-1)
    else:
        from validators import *
        user = User(
            tokens=db.tokens,
            debug='INFO'
        )
        user.set_blueprints(
            *commands_bp
        )
        user.run_polling(
            auto_reload=False,
            on_startup=lp_startup,
            on_shutdown=lp_shutdown
        )
