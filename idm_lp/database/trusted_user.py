import typing

from pydantic import BaseModel


class TrustedUser(BaseModel):
    user_id: int
    chat_id: typing.Optional[int] = None

