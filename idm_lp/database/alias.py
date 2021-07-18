from pydantic import BaseModel


class Alias(BaseModel):
    name: str
    command_from: str
    command_to: str
