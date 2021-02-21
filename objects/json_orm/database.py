import json
import os
from typing import List

import const
from logger import logger
from objects import (
    DotDict,
    IgnoredMembers,
    IgnoredGlobalMembers,
    MutedMembers,
    Alias,
    RolePlayCommand,
    ChatEnterModel, RegexDeleter
)
from objects.json_orm.checks import CheckClass
from objects.json_orm.errors import DatabaseWarning, DatabaseError
from objects.json_orm.loaders import Loaders
from objects.json_orm.mixins import ContextInstanceMixin
from objects.json_orm.savers import Savers
from objects.sloumo import SlouMo
from objects.trusted_user import TrustedUser


class Database(DotDict, ContextInstanceMixin):
    tokens: List[str]
    secret_code: str
    ru_captcha_key: str
    ignored_members: List[IgnoredMembers]
    ignored_global_members: List[IgnoredGlobalMembers]
    muted_members: List[MutedMembers]
    aliases: List[Alias]
    role_play_commands: List[RolePlayCommand]
    service_prefixes: List[str]
    self_prefixes: List[str]
    duty_prefixes: List[str]
    delete_all_notify: bool
    auto_exit_from_chat: bool
    auto_exit_from_chat_delete_chat: bool
    auto_exit_from_chat_add_to_black_list: bool
    disable_notifications: bool
    repeater_word: str
    repeater_active: str
    trusted: List[TrustedUser]
    add_to_friends_on_chat_enter: List[ChatEnterModel]
    sloumo: List[SlouMo]
    regex_deleter: List[RegexDeleter]

    __all_fields__ = [
        'tokens',
        'secret_code',
        'ru_captcha_key',
        'ignored_members',
        'ignored_global_members',
        'muted_members',
        'aliases',
        'role_play_commands',
        'service_prefixes',
        'self_prefixes',
        'duty_prefixes',
        'delete_all_notify',
        'auto_exit_from_chat',
        'auto_exit_from_chat_delete_chat',
        'auto_exit_from_chat_add_to_black_list',
        'add_to_friends_on_chat_enter',
        'disable_notifications',
        'sloumo',
        'repeater_word',
        'repeater_active',
        'trusted',
        'regex_deleter'
    ]

    loaders = Loaders()
    savers = Savers()

    def __init__(
            self,
            path_to_file: str,
            raw_data: dict,
            is_startup: bool = False
    ):
        super(Database, self).__init__(raw_data)
        self._path_to_file = path_to_file

        logger.debug(f"Путь до файла {self._path_to_file}")
        logger.debug("Загрузка базы данных...")
        for loader in self.loaders():
            setattr(self, loader.__name__, loader(raw_data))

        logger.debug("Выполнение проверки базы данных...")
        if is_startup:
            self.check_all()
        else:
            self.check()

    def save(self):
        self.check()
        data = dict(self)
        for saver in self.savers():
            data[saver.__name__] = saver(data)

        data_to_save = {}

        for key in data.keys():
            if key in self.__all_fields__:
                data_to_save[key] = data[key]

        with open(self._path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                json.dumps(
                    data_to_save,
                    ensure_ascii=False,
                    indent=2
                )
            )

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

    def check(self) -> None:
        checks = CheckClass.get_all_checks()
        issues = 0
        for cls in checks:
            if cls.only_startup:
                continue
            try:
                cls(self).check()
            except DatabaseWarning as ex:
                issues += 1
                logger.warning(f"Предупреждение \"{ex.name}\"\n{ex.description}")
            except DatabaseError as ex:
                logger.error(f"Ошибка \"{ex.name}\"\n{ex.description}")
                raise ex

        if not issues:
            logger.debug("Проверка базы данных не выявила проблем")
        else:
            logger.warning(f"При проверке базы данных выявлено {issues} проблем.")

    def check_all(self):
        checks = CheckClass.get_all_checks()
        issues = 0
        for cls in checks:
            logger.debug(f"Проверка {cls.__name__}")
            try:
                cls(self).check()
            except DatabaseWarning as ex:
                issues += 1
                logger.warning(f"Предупреждение \"{ex.name}\". {ex.description}")
            except DatabaseError as ex:
                logger.error(f"Ошибка \"{ex.name}\". {ex.description}")
                raise ex

        if not issues:
            logger.debug("Проверка базы данных не выявила проблем")
        else:
            logger.warning(f"При проверке базы данных выявлено {issues} проблем.")

    @staticmethod
    def load(is_startup: bool = False) -> 'Database':
        path_to_file = Database.get_path()
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                raw = json.loads(file.read())
        except FileNotFoundError:
            raw = const.DEFAULT_DATABASE
            with open(path_to_file, 'w', encoding='utf-8') as file:
                file.write(
                    json.dumps(
                        raw,
                        ensure_ascii=False,
                        indent=2
                    )
                )

        return Database(
            path_to_file,
            raw,
            is_startup
        )
