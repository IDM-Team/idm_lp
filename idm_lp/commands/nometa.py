import asyncio
import string
import time

from vkbottle import VKError
from vkbottle.framework.framework.rule import PrivateMessage
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.database import Database
from idm_lp.logger import logger_decorator
from idm_lp.utils import edit_message

user = Blueprint(
    name='nometa_blueprint'
)


def concat(element_list: list, postfix: str) -> list:
    for item in element_list:
        yield item + postfix


HELLO_TEXTS = [
    "привет", "ку", "салам",
    "приветствую", "здрасте", "здравствуйте",
    "здарова", "йоу", 'хай',
    'добрыйдень', 'доброеутро', 'добрыйвечер',
    'доброговременисуток', 'шалам', 'cаломалейкум',
    'cаламалейкум', 'салам', 'салом', "приветствуювас", "приветствую",
    "мыразделяемстобой солнце", "мыразделяемстобойлуну",
    'бонжур', 'привiт', 'hi', 'hello', 'здравствуй', 'приветик', 'хаюшки'
]

REPLACE_SYMBOLS = string.punctuation + " "

HELLO_STICKER_IDS = [

]


def levenshtein_distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


async def nometa_checker(db: Database, message: Message):
    await asyncio.sleep(db.nometa_delay)
    try:
        msgs = await message.api.messages.get_by_conversation_message_id(
            peer_id=message.peer_id,
            conversation_message_ids=[message.conversation_message_id + 1]
        )
        if msgs.items:
            return
    except VKError:
        pass

    await message.api.messages.send(
        peer_id=message.peer_id,
        message=db.nometa_message,
        attachment=",".join(db.nometa_attachments) if db.nometa_attachments else None,
        random_id=0
    )


@user.on.message_handler(FromMe(False), PrivateMessage())
@logger_decorator
async def nometa_message_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    if not db.nometa_enable:
        return

    text_to_scan = message.text.lower()
    for symb in REPLACE_SYMBOLS:
        text_to_scan = text_to_scan.replace(symb, '')

    if min(map(lambda x: levenshtein_distance(text_to_scan, x), HELLO_TEXTS)) > 3:
        return
    try:
        msgs = await message.api.messages.get_by_conversation_message_id(
            peer_id=message.peer_id,
            conversation_message_ids=[message.conversation_message_id - 1]
        )
        if msgs.items:
            time_prev = msgs.items[0].date
            if time.time() - time_prev < 60 * 60 * 12:
                return
    except (VKError, IndexError):
        pass

    asyncio.ensure_future(nometa_checker(db, message))


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -nometa")
@logger_decorator
async def activate_nometa_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.nometa_enable = False
    db.save()
    await edit_message(
        message,
        "✅ Режим NoMeta отключен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +nometa")
@logger_decorator
async def deactivate_nometa_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.nometa_enable = True
    db.save()
    await edit_message(
        message,
        "✅ Режим NoMeta включен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> nometa сообщение <text>")
@logger_decorator
async def deactivate_nometa_wrapper(message: Message, text: str, **kwargs):
    db = Database.get_current()
    db.nometa_message = text
    db.save()
    await edit_message(
        message,
        "✅ Текст NoMeta обновлен"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> nometa задержка <delay:float>")
@logger_decorator
async def deactivate_nometa_wrapper(message: Message, delay: float, **kwargs):
    db = Database.get_current()
    db.nometa_delay = delay
    db.save()
    await edit_message(
        message,
        "✅ Задержка NoMeta обновлена"
    )
