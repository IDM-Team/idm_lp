import asyncio
import json
import os
import typing
from typing import List
from idm_lp.logger import logger
from pydantic import BaseModel, validator, Field

from idm_lp import const
from . import (
    Alias,
    ChatEnterModel,
    IgnoredMembers,
    IgnoredGlobalMembers,
    MutedMembers,
    ContextInstanceMixin,
    RegexDeleter,
    RolePlayCommand,
    TrustedUser,
    SlouMo,
    DatabaseError
)


class Database(BaseModel, ContextInstanceMixin):
    # Не передаются на сервер, получаются либо с него (исключая токены и сервисные префиксы), либо с файла
    tokens: List[str] = Field([], to_server='exclude', from_server='exclude')
    secret_code: str = Field("", to_server='exclude', from_server='include')
    ru_captcha_key: typing.Optional[str] = Field("", to_server='exclude', from_server='include')
    service_prefixes: List[str] = Field([".слп", "!слп"], to_server='exclude', from_server='exclude')

    # Получаются исключительно с сервера
    repeater_word: str = Field("..", to_server='include', from_server='include')
    dd_prefix: str = Field("дд", to_server='include', from_server='include')

    auto_infection: bool = Field(False, to_server='include', from_server='include')
    auto_infection_interval: int = Field(3600, to_server='include', from_server='include')
    auto_infection_peer_id: int = Field(-174105461, to_server='include', from_server='include')
    auto_infection_argument: str = Field("р", to_server='include', from_server='include')

    bio_reply: bool = Field(False, to_server='include', from_server='include')
    repeater_active: bool = Field(False, to_server='include', from_server='include')

    delete_all_notify: bool = Field(False, to_server='include', from_server='include')
    auto_exit_from_chat: bool = Field(False, to_server='include', from_server='include')
    auto_exit_from_chat_delete_chat: bool = Field(False, to_server='include', from_server='include')
    auto_exit_from_chat_add_to_black_list: bool = Field(False, to_server='include', from_server='include')
    disable_notifications: bool = Field(False, to_server='include', from_server='include')

    nometa_enable: bool = Field(False, to_server='include', from_server='include')
    nometa_message: str = Field("nometa.xyz", to_server='include', from_server='include')
    nometa_attachments: List[str] = Field([], to_server='include', from_server='include')
    nometa_delay: float = Field(5 * 60, to_server='include', from_server='include')

    self_prefixes: List[str] = Field([".л", "!л"], to_server='include', from_server='include')
    duty_prefixes: List[str] = Field([".лд", "!лд"], to_server='include', from_server='include')

    ignored_members: List[IgnoredMembers] = Field([], to_server='include', from_server='include')
    ignored_global_members: List[IgnoredGlobalMembers] = Field([], to_server='include', from_server='include')
    muted_members: List[MutedMembers] = Field([], to_server='include', from_server='include')
    aliases: List[Alias] = Field([], to_server='include', from_server='include')
    role_play_commands: List[RolePlayCommand] = Field([], to_server='include', from_server='include')
    trusted: List[TrustedUser] = Field([], to_server='include', from_server='include')
    add_to_friends_on_chat_enter: List[ChatEnterModel] = Field([], to_server='include', from_server='include')
    sloumo: List[SlouMo] = Field([], to_server='include', from_server='include')
    regex_deleter: List[RegexDeleter] = Field([], to_server='include', from_server='include')

    __on_save_listeners: typing.List[typing.Callable] = []

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    @validator('tokens')
    def name_must_contain_space(cls, v):
        if not v:
            raise DatabaseError(
                name='Нет токенов',
                description='Укажите токены в файле конфигурации'
            )
        return v

    @staticmethod
    def get_path() -> str:
        if const.USE_APP_DATA:
            local_data_path = os.environ["APPDATA"]
            return os.path.abspath(
                os.path.join(
                    local_data_path,
                    "IDM",
                    const.CONFIG_PATH
                )
            )
        return os.path.abspath(const.CONFIG_PATH)

    @staticmethod
    def load() -> 'Database':
        path_to_file = Database.get_path()
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                db = Database(**json.loads(file.read()))
        except FileNotFoundError:
            db = None

        if not db:
            raise DatabaseError(
                'Конфиг не найден',
                f"Конфиг не найден по пути {path_to_file}"
            )

        if not db.tokens:
            raise DatabaseError(
                'Нет токенов',
                f"Укажите токены в файле конфигурации по пути {path_to_file}"
            )
        return db

    @classmethod
    def add_on_save(cls, func):
        cls.__on_save_listeners.append(func)
        return func

    def load_from_server(self, server_response: dict):
        for key, value in server_response.items():
            try:
                field = self.__fields__[key]
                extra = field.field_info.extra
                if extra['from_server'] == 'exclude':
                    continue
                setattr(self, key, value)
            except:
                pass
        self.save()
        logger.info("Конфиг загружен с сервера")

    def get_to_server(self):
        to_server = {}
        for key, value in self.dict().items():
            try:
                field = self.__fields__[key]
                extra = field.field_info.extra
                if extra['to_server'] == 'exclude':
                    continue
                to_server[key] = value
            except:
                pass
        return to_server

    def save(self):
        path_to_file = Database.get_path()
        for __on_save_listener in self.__on_save_listeners:
            asyncio.create_task(__on_save_listener(self))
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                self.json(include={'tokens', 'service_prefixes'}, **{"ensure_ascii": False, "indent": 2})
            )
