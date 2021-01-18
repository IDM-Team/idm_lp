from objects.dotdict import DotDict


class Alias(DotDict):
    name: str
    command_from: str
    command_to: str

    def save(self):
        return {
            'name': self.name,
            'command_from': self.command_from,
            'command_to': self.command_to
        }
