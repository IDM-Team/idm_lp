from typing import Optional, List, Iterable

from vkbottle import VKError
from vkbottle.api import UserApi
from vkbottle.user import Message

__all__ = (
    'edit_message',
    'get_id_by_domain',
    'get_ids_by_message',
    'get_full_name_by_member_id',
)


async def edit_message(
        message: Message,
        text: str = '',
        **kwargs
) -> int:
    """Простой редач сообщений
    Какие параметры пихать -- https://vk.com/dev/messages.edit

    :return: После успешного выполнения возвращает 1.
    """
    kwargs.setdefault('message_id', message.id)
    kwargs.setdefault('message', text)
    kwargs.setdefault('peer_id', message.peer_id)
    kwargs.setdefault('keep_forward_messages', True)
    kwargs.setdefault('keep_snippets', True)
    kwargs.setdefault('dont_parse_links', False)

    return await message.api.messages.edit(
        **kwargs
    )


async def get_id_by_domain(
        api: UserApi,
        domain: str,
        obj_types: Iterable[str] = ('user',)
) -> Optional[int]:
    """Определяет идентификатор обьекта по короткому имени

    :param api: АПИИИИИИИИИИИИИИИ
    :param domain: короткое имя
    :param obj_types: ID каких обьектов возвращать user, group, application
    """
    try:
        search = await api.utils.resolve_screen_name(screen_name=domain)
        if search.type in obj_types:
            return search.object_id if search.type == 'user' else -search.object_id
    except VKError:
        return None


async def get_ids_by_message(
        message: Message,
        member_id: Optional[int] = None,
        domain: Optional[str] = None
) -> List[int]:
    results = []

    if member_id:
        results.append(member_id)

    if domain:
        result = await get_id_by_domain(message.api, domain, ['user', 'group'])
        if result:
            results.append(result)

    if message.reply_message:
        results.append(message.reply_message.from_id)

    if message.fwd_messages:
        for fwd_msg in message.fwd_messages:
            results.append(fwd_msg.from_id)

    return results


async def get_full_name_by_member_id(
        api: UserApi,
        member_id: int
) -> str:
    """Полное имя по ID"""
    if member_id > 0:
        user = (await api.users.get(user_ids=member_id))[0]
        return f"{user.first_name} {user.last_name}"
    else:
        group = (await api.groups.get_by_id(group_ids=abs(member_id)))[0]
        return group.name
