from typing import List, Callable


class Savers:
    savers: List[Callable] = []

    def __init__(self):
        self.savers.append(self.ignored_members)
        self.savers.append(self.ignored_global_members)
        self.savers.append(self.muted_members)
        self.savers.append(self.aliases)
        self.savers.append(self.role_play_commands)
        self.savers.append(self.sloumo)
        self.savers.append(self.add_to_friends_on_chat_enter)
        self.savers.append(self.trusted)

    def __call__(self, *args, **kwargs):
        return self.savers

    @staticmethod
    def ignored_members(data: dict) -> List[dict]:
        return [
            ign_member.save()
            for ign_member in data['ignored_members']
        ]

    @staticmethod
    def sloumo(data: dict) -> List[dict]:
        return [
            slou.save()
            for slou in data['sloumo']
        ]

    @staticmethod
    def ignored_global_members(data: dict) -> List[dict]:
        return [
            ign_member.save()
            for ign_member in data['ignored_global_members']
        ]

    @staticmethod
    def muted_members(data: dict) -> List[dict]:
        return [
            muted_member.save()
            for muted_member in data['muted_members']
        ]

    @staticmethod
    def aliases(data: dict) -> List[dict]:
        return [
            alias.save()
            for alias in data['aliases']
        ]

    @staticmethod
    def role_play_commands(data: dict) -> List[dict]:
        return [
            role_play_command.save()
            for role_play_command in data['role_play_commands']
        ]

    @staticmethod
    def add_to_friends_on_chat_enter(data: dict) -> List[dict]:
        return [
            chat_enter_model.save()
            for chat_enter_model in data['add_to_friends_on_chat_enter']
        ]

    @staticmethod
    def trusted(data: dict) -> List[dict]:
        return [
            trusted_user.save()
            for trusted_user in data['trusted']
        ]

    @staticmethod
    def regex_deleter(data: dict) -> List[dict]:
        return [
            regex_del.save()
            for regex_del in data['regex_deleter']
        ]
