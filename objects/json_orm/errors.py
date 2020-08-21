

class DatabaseWarning(Exception):

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class DatabaseError(Exception):

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
