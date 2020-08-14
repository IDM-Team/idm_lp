from vkbottle.rule import AbstractMessageRule, Message

from objects import Database


class IgroredMembersRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.load()
        for ignore_member in db.igrored_members:
            if ignore_member.chat_id == message.peer_id and ignore_member.member_id == message.from_id:
                return True
        return False


class IgroredGlobalMembersRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.load()
        for ignore_member in db.igrored_global_members:
            if ignore_member.member_id == message.from_id:
                return True
        return False


class MutedMembersRule(AbstractMessageRule):

    async def check(self, message: Message) -> bool:
        db = Database.load()
        for muted_member in db.muted_members:
            if muted_member.chat_id == message.peer_id and muted_member.member_id == message.from_id:
                return True
        return False
