from typing import List, Callable


class Savers:
    savers: List[Callable] = []

    def __init__(self):
        self.savers.append(self.igrored_members)
        self.savers.append(self.igrored_global_members)
        self.savers.append(self.muted_members)
        self.savers.append(self.aliases)

    def __call__(self, *args, **kwargs):
        return self.savers

    @staticmethod
    def igrored_members(data: dict) -> List[dict]:
        return [
            ign_member.save()
            for ign_member in data['igrored_members']
        ]

    @staticmethod
    def igrored_global_members(data: dict) -> List[dict]:
        return [
            ign_member.save()
            for ign_member in data['igrored_global_members']
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
