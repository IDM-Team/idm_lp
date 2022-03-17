import typing

import aiohttp
import requests
from vkbottle.api import UserApi

from idm_lp.logger import logger
from idm_lp.database import ContextInstanceMixin, Database


class IDMException(Exception):
    ...


class IDMAPIException(IDMException):

    def __init__(self, code, detail, **kw):
        self.code = code
        self.detail = detail
        self.kwargs = kw

    def __str__(self):
        return f"[{self.code}] {self.detail}"


class IDMAPICallbackException(IDMException):
    CALLBACK_CODES = {
        1: "Пустой запрос",
        2: "Неизвестный тип сигнала",
        3: "Пара пользователь/секрет не найдены",
        4: "Беседа не привязана",
        5: "Пользователь заблокирован",
        6: "Дежурный не активен",
        7: "Пользователь не активен",
        10: "Не удалось связать беседу"
    }

    def __init__(
            self,
            response: str,
            error_code: typing.Optional[int] = None,
            error_message: typing.Optional[str] = None,
            **kw
    ):
        self.error_type = response
        self.error_code = error_code
        self.error_message = error_message
        self.kwargs = kw

    def __str__(self):
        if self.error_type == 'error':
            if self.error_code in self.CALLBACK_CODES:
                return f"[{self.error_code}] {self.CALLBACK_CODES[self.error_code]}"
            elif self.error_message:
                return f"[{self.error_code}] {self.error_message}"
            else:
                return f"[{self.error_code}] Нe известная ошибка"
        else:
            if self.error_message:
                return f"VK [{self.error_code}] {self.error_message}"
            else:
                return f"VK [{self.error_code}] Нe известная ошибка"


class IDMAPI(ContextInstanceMixin):
    _session: typing.Optional[aiohttp.ClientSession]
    _sync_session: typing.Optional[requests.Session]

    def __init__(self, base_domain: str, header: str):
        self.base_domain = base_domain
        self.header_info = header
        self._session = None
        self._sync_session = None

        self._get_lp_info_link = f"{self.base_domain}/api/dutys/get_lp_info/"
        self._save_lp_info_link = f"{self.base_domain}/api/dutys/save_lp_info/"
        self._callback_link = f"{self.base_domain}/callback/"

    @property
    def sync_session(self) -> requests.Session:
        if not self._sync_session:
            self._sync_session = requests.Session()
        return self._sync_session

    @property
    def session(self):
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(headers={"User-Agent": self.header_info})
        return self._session

    def get_lp_info_sync(self, access_token: str) -> dict:
        response = self.sync_session.post(
            self._get_lp_info_link,
            json={'access_token': access_token},
            headers={'User-Agent': self.header_info}
        ).json()
        if 'error' in response:
            raise IDMAPIException(**response['error'])
        return response['response']

    async def send_request(self, url: str, data: dict) -> dict:
        logger.debug(f"Send POST request to {url} with data {data!r}")
        async with self.session.post(url, json=data) as response:
            response_json = await response.json()
            logger.debug(f"Response from {url}: {response_json!r}")

            if 'error' in response_json:
                raise IDMAPIException(**response_json['error'])
            if response_json['response'] in ('error', 'vk_error',):
                raise IDMAPICallbackException(**response_json)
            return response_json

    async def get_lp_info(self, access_token: str):
        response = await self.send_request(self._get_lp_info_link, {'access_token': access_token})
        return response['response']

    async def save_lp_info(self, access_token: str, database: dict):
        response = await self.send_request(self._save_lp_info_link, {
            'access_token': access_token,
            'config': database
        })
        return response['response']

    async def callback(self, data: dict) -> dict:
        api = UserApi.get_current()
        db = Database.get_current()

        data['user_id'] = await api.user_id
        data['secret'] = db.secret_code

        return await self.send_request(self._callback_link, data)

    async def ping(self):
        return await self.callback({
            "method": "ping",
            "message": {},
            "object": {}
        })

    async def _send_signal(
            self,
            method: str,
            from_id: int,
            peer_id: int,
            conversation_message_id: int,
            date: int,
            text: str,
            vk_message: typing.Optional[dict] = None
    ):
        return await self.callback({
            "method": method,
            "message": {
                "conversation_message_id": conversation_message_id,
                "from_id": from_id,
                "date": date,
                "text": text,
                "peer_id": peer_id
            },
            "object": {
                "chat": None,
                "from_id": from_id,
                "value": text,
                "conversation_message_id": conversation_message_id
            },
            "vkmessage": vk_message
        })

    async def send_my_signal(
            self,
            from_id: int,
            peer_id: int,
            conversation_message_id: int,
            date: int,
            text: str,
            vk_message: typing.Optional[dict] = None
    ):
        return await self._send_signal(
            'lpSendMySignal',
            from_id=from_id, peer_id=peer_id,
            conversation_message_id=conversation_message_id,
            date=date, text=text, vk_message=vk_message
        )

    async def send_signal(
            self,
            from_id: int,
            peer_id: int,
            conversation_message_id: int,
            date: int,
            text: str,
            vk_message: typing.Optional[dict] = None
    ):
        return await self._send_signal(
            'lpSendSignal',
            from_id=from_id, peer_id=peer_id,
            conversation_message_id=conversation_message_id,
            date=date, text=text, vk_message=vk_message
        )
