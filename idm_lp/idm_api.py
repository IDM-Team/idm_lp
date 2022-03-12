import typing

import aiohttp

from idm_lp.database import ContextInstanceMixin


class IDMAPI(ContextInstanceMixin):
    _session: typing.Optional[aiohttp.ClientSession]

    def __init__(self, base_domain: str, header: str):
        self.base_domain = base_domain
        self.header_info = header
        self._session = None

        self._get_lp_info_link = f"{self.base_domain}/api/dutys/get_lp_info/"
        self._save_lp_info_link = f"{self.base_domain}/api/dutys/save_lp_info/"

    @property
    def session(self):
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(headers={"User-Agent": self.header_info})
        return self._session

    async def get_lp_info(self, access_token: str):
        async with self.session.post(self._get_lp_info_link, json={'access_token': access_token}) as response:
            response_data = await response.json()
            if 'error' in response_data:
                raise Exception(response_data['error']['detail'])
            return response_data['response']

    async def save_lp_info(self, access_token: str, database: dict):
        async with self.session.post(self._save_lp_info_link, json={
            'access_token': access_token,
            'config': database
        }) as response:
            response_data = await response.json()
            if 'error' in response_data:
                raise Exception(response_data['error']['detail'])
            return response_data['response']
