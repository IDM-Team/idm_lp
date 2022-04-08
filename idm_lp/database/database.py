import asyncio
import json
import os
import typing

from pydantic import BaseModel, validator, Field

from idm_lp import const
from . import (
    Alias,
    ChatEnterModel,
    IgnoredMembers,
    MutedMembers,
    ContextInstanceMixin,
    RegexDeleter,
    RolePlayCommand,
    TrustedUser,
    DatabaseError,
    Timer
)


class Database(BaseModel, ContextInstanceMixin):
    # Не передаются на сервер, получаются либо с него (исключая токены и сервисные префиксы), либо с файла
    tokens: typing.List[str] = Field([], to_server='exclude', from_server='exclude')
    secret_code: str = Field("", to_server='exclude', from_server='include')
    ru_captcha_key: typing.Optional[str] = Field("", to_server='exclude', from_server='include')
    service_prefixes: typing.List[str] = Field([".слп", "!слп"], to_server='exclude', from_server='exclude')

    # Получаются исключительно с сервера
    repeater_word: str = Field("..", to_server='include', from_server='include')
    dd_prefix: str = Field("дд", to_server='include', from_server='include')
    editor_prefix: str = Field("рр", to_server='include', from_server='include')

    timers: typing.List[Timer] = Field([], to_server='include', from_server='include')

    auto_infection: bool = Field(False, to_server='include', from_server='include')
    auto_infection_interval: int = Field(3600, to_server='include', from_server='include')
    auto_infection_peer_id: int = Field(-174105461, to_server='include', from_server='include')
    auto_infection_argument: str = Field("р", to_server='include', from_server='include')

    bio_reply: bool = Field(False, to_server='include', from_server='include')
    auto_vaccine: bool = Field(False, to_server='include', from_server='include')
    repeater_active: bool = Field(False, to_server='include', from_server='include')

    delete_all_notify: bool = Field(False, to_server='include', from_server='include')
    auto_exit_from_chat: bool = Field(False, to_server='include', from_server='include')
    auto_exit_from_chat_delete_chat: bool = Field(False, to_server='include', from_server='include')
    auto_exit_from_chat_add_to_black_list: bool = Field(False, to_server='include', from_server='include')
    disable_notifications: bool = Field(False, to_server='include', from_server='include')

    nometa_enable: bool = Field(False, to_server='include', from_server='include')
    nometa_message: str = Field("nometa.xyz", to_server='include', from_server='include')
    nometa_attachments: typing.List[str] = Field([], to_server='include', from_server='include')
    nometa_delay: float = Field(5 * 60, to_server='include', from_server='include')

    self_prefixes: typing.List[str] = Field([".л", "!л"], to_server='include', from_server='include')
    duty_prefixes: typing.List[str] = Field([".лд", "!лд"], to_server='include', from_server='include')

    ignored_members: typing.List[IgnoredMembers] = Field([], to_server='include', from_server='include')
    muted_members: typing.List[MutedMembers] = Field([], to_server='include', from_server='include')
    aliases: typing.List[Alias] = Field([], to_server='include', from_server='include')
    role_play_commands: typing.List[RolePlayCommand] = Field([], to_server='include', from_server='include')
    trusted: typing.List[TrustedUser] = Field([], to_server='include', from_server='include')
    add_to_friends_on_chat_enter: typing.List[ChatEnterModel] = Field([], to_server='include', from_server='include')
    regex_deleter: typing.List[RegexDeleter] = Field([], to_server='include', from_server='include')

    spy_check_online: typing.List[int] = Field([], to_server='include', from_server='include')
    spy_check_typing: typing.List[int] = Field([], to_server='include', from_server='include')
    spy_check_messages: typing.List[int] = Field([], to_server='include', from_server='include')

    __on_save_listeners: typing.List[typing.Callable] = []

    @validator('service_prefixes')
    def service_prefixes_validator(cls, v: typing.List[str]) -> typing.List[str]:
        if not v:
            return ['!слп', '.слп']
        return list(set([x.lower() for x in v]))

    @validator('self_prefixes')
    def self_prefixes_validator(cls, v: typing.List[str]) -> typing.List[str]:
        if not v:
            return [".л", "!л"]
        return list(set([x.lower() for x in v]))

    @validator('duty_prefixes')
    def duty_prefixes_validator(cls, v: typing.List[str]) -> typing.List[str]:
        if not v:
            return [".лд", "!лд"]
        return list(set([x.lower() for x in v]))

    @validator('repeater_word', 'dd_prefix')
    def to_lower_validator(cls, v: str) -> str:
        return v.lower()

    @validator('spy_check_online', 'spy_check_typing', 'spy_check_messages', 'tokens')
    def unique_validator(cls, v: typing.List) -> typing.List:
        return list(set(v))

    @property
    def ignored_global_members(self):
        return [x for x in self.ignored_members if x.chat_id is None]

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

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
            db = Database.parse_file(path_to_file)
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

    def load_from_server(self):
        from ..idm_api import IDMAPI
        new_config = IDMAPI.get_current().get_lp_info_sync(self.tokens[0])['config']
        new_database = {
            "tokens": self.tokens,
            "service_prefixes": self.service_prefixes,
            "secret_code": self.secret_code,
            **new_config
        }
        return Database.parse_obj(new_database)

    def get_to_server(self):
        to_server = {}
        for key, value in json.loads(self.json()).items():
            try:
                field = self.__fields__[key]
                extra = field.field_info.extra
                if extra['to_server'] == 'exclude':
                    continue
                to_server[key] = value
            except KeyError:
                pass
        return to_server

    def save(self):
        path_to_file = Database.get_path()
        for __on_save_listener in self.__on_save_listeners:
            asyncio.create_task(__on_save_listener(self))

        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                self.json(exclude={'__on_save_listeners'}, **{"ensure_ascii": False, "indent": 2})
            )
