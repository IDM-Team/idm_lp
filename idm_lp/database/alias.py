from pydantic import BaseModel, validator


class Alias(BaseModel):
    name: str
    command_from: str
    command_to: str

    @validator('name')
    def to_lower_validator(cls, v: str) -> str:
        return v.lower()

    @property
    def regexp(self) -> str:
        _regexp_control = r"[]\/^$.|?*+-(){}"
        command_from = self.command_from[:]
        for control in _regexp_control:
            command_from = command_from.replace(control, "\\" + control)
        return command_from
