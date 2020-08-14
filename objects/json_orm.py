import json
import os
import platform
from typing import List

from const import DEFAULT_DATABASE
from objects import (
    DotDict,
    IgroredMembers,
    IgroredGlobalMembers,
    MutedMembers,
    Alias
)

__all__ = (
    'Database',
)


class Database(DotDict):
    # структура
    tokens: List[str]
    secret_code: str
    igrored_members: List[IgroredMembers]
    igrored_global_members: List[IgroredGlobalMembers]
    muted_members: List[MutedMembers]
    aliases: List[Alias]
    service_prefixes: List[str]
    self_prefixes: List[str]
    duty_prefixes: List[str]

    # Служебные поля
    _all_keys = (
        'tokens',
        'secret_code',
        'igrored_members',
        'igrored_global_members',
        'muted_members',
        'aliases',
        'service_prefixes',
        'self_prefixes',
        'duty_prefixes'
    )

    class DatabaseError(Exception):
        pass

    class KeyNotFoundError(DatabaseError):

        def __init__(self, key: str, all_keys: List[str]):
            self.key = key
            self.all_keys = all_keys

        def __repr__(self):
            return f"<KeyNotFoundError({self.key}, {self.all_keys})>"

        def __str__(self):
            return f"Ключ {self.key} не найден в базе данных"

    class SmallAmountTokensError(DatabaseError):
        def __init__(self, count):
            self.count = count

        def __repr__(self):
            return f"<SmallAmountTokensError({self.count})>"

        def __str__(self):
            return f"Малое количество токенов -- {self.count}. Необходимо 3 и больше."

    def __init__(
            self,
            path_to_file: str = 'config.json',
            raw_data: dict = {}
    ):
        super().__init__(raw_data)
        self._path_to_file = path_to_file
        self.igrored_members = [IgroredMembers(igrored_member) for igrored_member in self.igrored_members]
        self.igrored_global_members = [
            IgroredGlobalMembers(igrored_global_member)
            for igrored_global_member in self.igrored_global_members
        ]
        self.muted_members = [MutedMembers(muted_member) for muted_member in self.muted_members]
        self.aliases = [Alias(alias) for alias in self.aliases]
        self.check_all()

    def __check_db_keys__(self):
        for key in self._all_keys:
            if key not in self.keys():
                raise Database.KeyNotFoundError(key=key, all_keys=list(self.keys()))

    def __check_token_count__(self):
        if not self.tokens or len(self.tokens) < 3:
            raise Database.SmallAmountTokensError(0 if not self.tokens else len(self.tokens))

    @staticmethod
    def get_path():
        # if 'win' in platform.system().lower():
        #     local_data_path = os.environ["APPDATA"]
        #     return os.path.join(
        #         local_data_path,
        #         'IDM',
        #         'config.json'
        #     )
        # else:
        return 'config.json'

    @staticmethod
    def load() -> "Database":
        """
        Загружает значение из базы
        """
        path_to_file = Database.get_path()
        with open(path_to_file, 'r', encoding='utf-8') as file:
            raw = json.loads(file.read())
            return Database(path_to_file, raw)

    @staticmethod
    def recreate() -> "Database":
        path_to_file = Database.get_path()
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                json.dumps(
                    DEFAULT_DATABASE,
                    ensure_ascii=False,
                    indent=2
                )
            )
        return Database.load()

    def save(self) -> None:
        self.check_all()

        raw = {}
        raw.update(tokens=self.save_tokens)
        raw.update(secret_code=self.save_secret_code)
        raw.update(igrored_members=self.save_igrored_members)
        raw.update(igrored_global_members=self.save_igrored_global_members)
        raw.update(muted_members=self.save_muted_members)
        raw.update(aliases=self.save_aliases)

        raw.update(service_prefixes=self.save_service_prefixes)
        raw.update(self_prefixes=self.save_self_prefixes)
        raw.update(duty_prefixes=self.save_duty_prefixes)

        with open(self._path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                json.dumps(
                    raw,
                    ensure_ascii=False,
                    indent=2
                )
            )

    def check_all(self) -> None:
        for key in dir(self):
            if key.startswith('__check_'):
                self.__getattribute__(key)()

    @property
    def save_tokens(self) -> List[str]:
        return self.tokens

    @property
    def save_secret_code(self) -> str:
        return self.secret_code

    @property
    def save_aliases(self) -> List[dict]:
        data = []
        for alias in self.aliases:
            data.append(alias.save())
        return data

    @property
    def save_igrored_members(self) -> List[dict]:
        data = []
        for igrored_member in self.igrored_members:
            data.append(igrored_member.save())
        return data

    @property
    def save_igrored_global_members(self) -> List[dict]:
        data = []
        for igrored_global_member in self.igrored_global_members:
            data.append(igrored_global_member.save())
        return data

    @property
    def save_muted_members(self) -> List[dict]:
        data = []
        for muted_member in self.muted_members:
            data.append(muted_member.save())
        return data

    @property
    def save_service_prefixes(self) -> List[str]:
        return self.service_prefixes

    @property
    def save_self_prefixes(self) -> List[str]:
        return self.self_prefixes

    @property
    def save_duty_prefixes(self) -> List[str]:
        return self.duty_prefixes
