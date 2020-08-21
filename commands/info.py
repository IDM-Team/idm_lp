from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from const import __version__, __author__

from objects import Database

user = Blueprint(
    name='info_blueprint'
)


@user.on.message(FromMe(), text="<prefix:service_prefix> инфо")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> инфо")
async def ping_wrapper(message: Message, **kwargs):
    db = Database.load()
    text = f"""
    IDM LP v{__version__} by {__author__}

    Ключ рукаптчи: {"&#9989;" if db.ru_captcha_key else "&#10060;"}

    В игноре: {len(db.igrored_members)}
    В глобальном игноре: {len(db.igrored_global_members)}
    В муте: {len(db.muted_members)}
    Алиасов: {len(db.aliases)}
    
    Сервисные префиксы: {' '.join(db.service_prefixes)}
    Свои префиксы: {' '.join(db.self_prefixes) if db.self_prefixes else ''}
    Префиксы дежурного: {' '.join(db.duty_prefixes) if db.duty_prefixes else ''}
    """.replace('    ', '')
    await message(text)
