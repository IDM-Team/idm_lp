from typing import Optional, List, Iterable

import aiohttp
from vkbottle import VKError
from vkbottle.api import UserApi
from vkbottle.user import Message

from idm_lp import const
from idm_lp import logger

__all__ = (
    'edit_message',
    'get_id_by_domain',
    'get_ids_by_message',
    'get_full_name_by_member_id',
    'send_request',
    'check_ping'
)


async def send_request(request_data: dict):
    logger.logger.debug(f"Send request to server with data: {request_data}")
    api = UserApi.get_current()
    message = ""
    async with aiohttp.ClientSession(headers={"User-Agent": const.APP_USER_AGENT}) as session:
        async with session.post(const.CALLBACK_LINK(), json=request_data) as resp:
            if resp.status != 200:
                message = f"⚠ Ошибка сервера IDM Multi. Сервер, ответил кодом {resp.status}."
            else:
                data_json = await resp.json()
                if data_json['response'] == 'ok':
                    return
                elif data_json['response'] == "error":
                    if data_json.get('error_code') == 1:
                        message = f"⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Пустой запрос>>"
                    elif data_json.get('error_code') == 2:
                        message = f"⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Неизвестный тип сигнала>>"
                    elif data_json.get('error_code') == 3:
                        message = (
                            f"⚠ Ошибка сервера IDM Multi. "
                            f"Сервер, ответил: <<Пара пользователь/секрет не найдены>>"
                        )
                    elif data_json.get('error_code') == 4:
                        message = f"⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Беседа не привязана>>"
                    elif data_json.get('error_code') == 10:
                        message = f"⚠ Ошибка сервера IDM Multi. Сервер, ответил: <<Не удалось связать беседу>>"
                    else:
                        message = (
                            f"⚠ Ошибка сервера IDM Multi. "
                            f"Сервер, ответил: <<Ошибка #{data_json.get('error_code')}>>"
                        )
                elif data_json['response'] == "vk_error":
                    message = (
                        f"⚠ Ошибка сервера IDM Multi. "
                        f"Сервер, ответил: "
                        f"<<Ошибка VK #{data_json.get('error_code')} {data_json.get('error_message', '')}>>"
                    )
    if message:
        await api.messages.send(
            random_id=0,
            peer_id=await api.user_id,
            message=message
        )


async def check_ping(secret_code: str):
    await send_request({
        "user_id": await UserApi.get_current().user_id,
        "method": "ping",
        "secret": secret_code,
        "message": {},
        "object": {}
    })


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
