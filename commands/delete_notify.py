from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from objects import Database
from rules import DeleteNotifyRule
from utils import edit_message

user = Blueprint(
    name='delete_notify_blueprint'
)


@user.on.chat_message(DeleteNotifyRule())
@user.on.message(DeleteNotifyRule())
async def delete_notify_wrapper(message: Message):
    await message.api.messages.delete(message_ids=[message.id])


@user.on.chat_message(FromMe(), text="<prefix:service_prefix> -уведы")
@user.on.message(FromMe(), text="<prefix:service_prefix> -уведы")
async def activate_delete_all_notify_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.delete_all_notify = True
    db.save()
    await edit_message(
        message,
        "✅ Удаление уведомлений включено"
    )


@user.on.chat_message(FromMe(), text="<prefix:service_prefix> +уведы")
@user.on.message(FromMe(), text="<prefix:service_prefix> +уведы")
async def deactivate_delete_all_notify_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.delete_all_notify = False
    db.save()
    await edit_message(
        message,
        "✅ Удаление уведомлений отключено"
    )
