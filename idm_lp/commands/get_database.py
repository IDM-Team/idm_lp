import aiohttp
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp import const
from idm_lp.database import Database
from idm_lp.logger import logger_decorator
from idm_lp.utils import edit_message

user = Blueprint(
    name='set_db_blueprint'
)


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> получить бд")
@logger_decorator
async def set_db_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    async with aiohttp.ClientSession(headers={"User-Agent": const.APP_USER_AGENT}) as session:
        async with session.post(const.GET_LP_INFO_LINK(), json={'access_token': db.tokens[0]}) as resp:
            response = await resp.json()
            if 'error' in response:
                await message.api.messages.send(
                    peer_id=await message.api.user_id,
                    random_id=0,
                    message=f"⚠ Ошибка: {response['error']['detail']}"
                )
                raise KeyboardInterrupt()
            else:
                if not response['response']['is_active']:
                    await message.api.messages.send(
                        peer_id=await message.api.user_id,
                        random_id=0,
                        message=f"⚠ Ошибка: дежурный не активен"
                    )
                    raise KeyboardInterrupt()
                database = Database.parse_obj(response['response']['config'])
                Database.set_current(database)
                database.save(True)
    await edit_message(
        message,
        "OK"
    )
