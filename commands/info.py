import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

import const
from const import __version__, __author__

from objects import Database

user = Blueprint(
    name='info_blueprint'
)


@user.on.message(FromMe(), text="<prefix:service_prefix> инфо")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> инфо")
async def ping_wrapper(message: Message, **kwargs):
    db = Database.load()

    version_rest = requests.get(const.VERSION_REST).json()

    if version_rest['version'] != const.__version__:
        update_text = f"\n\n Доступно обновление {version_rest['version']}\n" \
                      f"{version_rest['description']}\n"
    else:
        update_text = ""

    text = f"""
    IDM LP v{__version__} by {__author__}

    Ключ рукаптчи: {"&#9989;" if db.ru_captcha_key else "&#10060;"}

    В игноре: {len(db.igrored_members)}
    В глобальном игноре: {len(db.igrored_global_members)}
    В муте: {len(db.muted_members)}
    Алиасов: {len(db.aliases)}
    
    Сервисные префиксы: {' '.join(db.service_prefixes)}
    Свои префиксы: {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    Префиксы дежурного: {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}{update_text}
    """.replace('    ', '')
    await message(text)
