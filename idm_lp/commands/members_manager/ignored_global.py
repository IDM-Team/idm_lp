from vkbottle.api import UserApi
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database, IgnoredMembers
from idm_lp.utils import edit_message, get_ids_by_message, get_full_name_by_member_id, generate_user_or_groups_list

user = Blueprint(
    name='ignored_global_members_blueprint'
)


def add_ignore_global_member(database: Database, member_id: int) -> None:
    database.ignored_members.append(
        IgnoredMembers(
            member_id=member_id,
            chat_id=None
        )
    )
    database.save()


def remove_ignore_global_member(database: Database, member_id: int) -> None:
    ignored_member = None
    for ign in database.ignored_global_members:
        if ign.member_id == member_id:
            ignored_member = ign
    database.ignored_members.remove(ignored_member)
    database.save()


async def show_ignore_global_members(
        database: Database,
        api: UserApi
) -> str:
    user_ids = [
        ignore_member.member_id
        for ignore_member in database.ignored_global_members
        if ignore_member.member_id > 0
    ]
    group_ids = [
        abs(ignore_member.member_id)
        for ignore_member in database.ignored_global_members
        if ignore_member.member_id < 0
    ]

    if not user_ids and not group_ids:
        return "📃 Ваш глобальный игнор-лист пуст"

    message = "📃 Ваш глобальный игнор-лист\n"
    return await generate_user_or_groups_list(api, message, user_ids, group_ids)


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> +глоигнор [id<user_id:int>|<foo>',
        '<prefix:service_prefix> +глоигнор [club<group_id:int>|<foo>',
        '<prefix:service_prefix> +глоигнор https://vk.com/<domain>',
        '<prefix:service_prefix> +глоигнор',
    ]
)
@logger_decorator
async def add_ignored_global_member_wrapper(
        message: Message,
        domain: str = None,
        user_id: int = None,
        group_id: int = None,
        **kwargs
):
    db = Database.get_current()
    member_id = user_id if user_id else None
    if not user_id and group_id:
        member_id = -group_id

    member_ids = await get_ids_by_message(message, member_id, domain)
    if not member_ids:
        await edit_message(
            message,
            f'⚠ Необходимо указать пользователей'
        )
        return

    member_id = member_ids[0]
    if member_id == await message.api.user_id:
        await edit_message(
            message,
            f'⚠ Нельзя занести себя в игнор!'
        )
        return

    if member_id > 0:
        name = f'Пользователь  [id{member_id}|{await get_full_name_by_member_id(message.api, member_id)}]'
    else:
        name = f'Группа [club{abs(member_id)}|{await get_full_name_by_member_id(message.api, member_id)}]'

    if member_id in [
        igrored_member.member_id
        for igrored_member in db.ignored_global_members
    ]:
        await edit_message(
            message,
            f'⚠ {name} уже в списке игнорируемых'
        )
        return
    add_ignore_global_member(db, member_id)
    await edit_message(
        message,
        f'✅ {name} добавлен в глобальный игнор-лист'
    )


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> -глоигнор [id<user_id:int>|<foo>',
        '<prefix:service_prefix> -глоигнор [club<group_id:int>|<foo>',
        '<prefix:service_prefix> -глоигнор https://vk.com/<domain>',
        '<prefix:service_prefix> -глоигнор',
    ]
)
@logger_decorator
async def remove_ignored_global_member_wrapper(
        message: Message,
        domain: str = None,
        user_id: int = None,
        group_id: int = None,
        **kwargs
):
    db = Database.get_current()
    member_id = user_id if user_id else None
    if not user_id and group_id:
        member_id = -group_id

    member_ids = await get_ids_by_message(message, member_id, domain)
    if not member_ids:
        await edit_message(
            message,
            f'⚠ Необходимо указать пользователей'
        )
        return

    member_id = member_ids[0]

    if member_id > 0:
        name = f'Пользователь  [id{member_id}|{await get_full_name_by_member_id(message.api, member_id)}]'
    else:
        name = f'Группа [club{abs(member_id)}|{await get_full_name_by_member_id(message.api, member_id)}]'

    if member_id not in [
        igrored_member.member_id
        for igrored_member in db.ignored_global_members
    ]:
        await edit_message(
            message,
            f'⚠ {name} не в списке игнорируемых'
        )
        return
    remove_ignore_global_member(db, member_id)
    await edit_message(
        message,
        f'✅ {name} удален из игнор-листа'
    )


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> глоигнорлист',
        '<prefix:service_prefix> глоигнор лист',
    ]
)
@logger_decorator
async def show_ignore_members_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await edit_message(
        message,
        await show_ignore_global_members(
            db,
            message.api
        )
    )
