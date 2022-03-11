import asyncio
import json
import os
import typing
from typing import List

from pydantic import BaseModel, validator

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
    secret_code: str = ""
    ru_captcha_key: typing.Optional[str] = ""
    repeater_word: str = ".."
    dd_prefix: str = "дд"

    auto_infection: bool = False
    auto_infection_interval: int = 3600
    auto_infection_peer_id: int = -174105461
    auto_infection_argument: str = "р"

    bio_reply: bool = False
    repeater_active: bool = False

    delete_all_notify: bool = False
    auto_exit_from_chat: bool = False
    auto_exit_from_chat_delete_chat: bool = False
    auto_exit_from_chat_add_to_black_list: bool = False
    disable_notifications: bool = False

    nometa_enable: bool = False
    nometa_message: str = "nometa.xyz"
    nometa_attachments: List[str] = []
    nometa_delay: float = 5 * 60

    tokens: List[str] = []
    service_prefixes: List[str] = [".слп", "!слп"]
    self_prefixes: List[str] = [".л", "!л"]
    duty_prefixes: List[str] = [".лд", "!лд"]

    ignored_members: List[IgnoredMembers] = []
    ignored_global_members: List[IgnoredGlobalMembers] = []
    muted_members: List[MutedMembers] = []
    aliases: List[Alias] = []
    role_play_commands: List[RolePlayCommand] = []
    trusted: List[TrustedUser] = []
    add_to_friends_on_chat_enter: List[ChatEnterModel] = []
    sloumo: List[SlouMo] = []
    regex_deleter: List[RegexDeleter] = []

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

    def save(self, force_listeners: bool = False):
        path_to_file = Database.get_path()
        for __on_save_listener in self.__on_save_listeners:
            asyncio.create_task(__on_save_listener(self))
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                self.json(exclude={'__on_save_listeners'}, **{"ensure_ascii": False, "indent": 2})
            )
