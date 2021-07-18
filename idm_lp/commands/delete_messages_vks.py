import datetime

from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.utils import edit_message

user = Blueprint(
    name='delete_messages_vks_blueprint'
)

DD_SCRIPT = (
    'var i = 0;var msg_ids = [];var count = %d;'
    'var items = API.messages.getHistory({"peer_id":%d,"count":"200", "offset":"0"}).items;'
    'while (count > 0 && i < items.length) {if (items[i].out == 1) {if (items[i].id == %d) {'
    'if (items[i].reply_message) {msg_ids.push(items[i].id);msg_ids.push(items[i].reply_message.id);'
    'count = 0;};if (items[i].fwd_messages) {msg_ids.push(items[i].id);var j = 0;while (j < '
    'items[i].fwd_messages.length) {msg_ids.push(items[i].fwd_messages[j].id);j = j + 1;};count = 0;};};'
    'msg_ids.push(items[i].id);count = count - 1;};if ((%d - items[i].date) > 86400) {count = 0;};i = i + 1;};'
    'API.messages.delete({"message_ids": msg_ids,"delete_for_all":"1"});return count;'
)


@user.on.message_handler(
    FromMe(),
    text=["<count:dd_value>", "<s:dd_prefix>"],
)
@logger_decorator
async def dd_handler(message: Message, count: int = 2, **kwargs):
    count += 1
    await message.api.execute(
        DD_SCRIPT % (
            count,
            message.peer_id,
            message.from_id,
            int(datetime.datetime.now().timestamp())
        )
    )


@user.on.message_handler(
    FromMe(),
    text=["<s:dd_prefix> все", "<s:dd_prefix> всё"],
)
@logger_decorator
async def dd_all_handler(message: Message, **kwargs):
    count = 1000
    await message.api.execute(
        DD_SCRIPT % (
            count,
            message.peer_id,
            message.from_id,
            int(datetime.datetime.now().timestamp())
        )
    )


@user.on.message_handler(
    FromMe(),
    text="<s:service_prefix> дд префикс <prefix>",
)
@logger_decorator
async def set_dd_prefix_handler(message: Message, prefix: str, **kwargs):
    db = Database.get_current()
    db.dd_prefix = prefix
    db.save()
    await edit_message(
        message,
        f"✅ Префикс дд установлен на <<{db.dd_prefix}>>"
    )
