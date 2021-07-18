import re
from typing import List, Union

from vkbottle.rule import AbstractMessageRule, Message

from idm_lp.database import Database


class DeleteNotifyRule(AbstractMessageRule):
    notify_all_words = [
        'all',
        'online',
        'here',
        'everyone',

        'все',
        'онлайн',
        'здесь',
        'тут',
    ]

    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        if not db.delete_all_notify:
            return False

        if any([f"@{i}" in message.text.lower() for i in self.notify_all_words]):
            return True
        return False


class ChatEnterRule(AbstractMessageRule):
    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        for chat_enter_model in db.add_to_friends_on_chat_enter:
            if chat_enter_model.peer_id == message.peer_id:
                return True
        return False


class IgnoredMembersRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        for ignore_member in db.ignored_members:
            if ignore_member.chat_id == message.peer_id and ignore_member.member_id == message.from_id:
                return True
        return False


class IgnoredGlobalMembersRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        for ignore_member in db.ignored_global_members:
            if ignore_member.member_id == message.from_id:
                return True
        return False


class MutedMembersRule(AbstractMessageRule):

    async def check(self, message: Message):
        db = Database.get_current()
        for muted_member in db.muted_members:
            if muted_member.chat_id == message.peer_id and muted_member.member_id == message.from_id:
                return dict(member=muted_member)
        return False


class SlouMoRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        for slou in db.sloumo:
            if slou.chat_id == message.chat_id:
                return True
        return False


class TrustedRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        for trusted in db.trusted:
            if trusted.user_id == message.from_id:
                return True
        return False


class RegexDeleter(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.get_current()
        for regex_del in db.regex_deleter:
            if regex_del.chat_id == message.peer_id:
                if re.findall(regex_del.regex, message.text):
                    return True
        return False


class ContainsRule(AbstractMessageRule):

    def __init__(self, words: Union[str, List[str]], not_include: List[str] = [], upper: bool = True):
        self.words = words if isinstance(words, list) else [words]
        self.not_include = not_include if isinstance(not_include, list) else [not_include]
        self.upper = upper

    async def check(self, message: Message) -> bool:
        checked = False
        for word in self.words:
            if word.upper() in message.text.upper():
                checked = True
        for ni_word in self.not_include:
            if ni_word.upper() in message.text.upper():
                checked = False
        return checked
