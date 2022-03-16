import enum
import typing
import uuid
from datetime import datetime

import pydantic

from idm_lp.utils import parse_cron_text


class TimerType(enum.Enum):
    """
    AT_DATE - выполняется один раз, в какое-то время например 24.06.2023 в 20:20:21
    INTERVAL - выполняется каждые N секунд
    EVERY_DATE - выполняется каждый месяц, 4 числа в 20:20:21
    """
    DATE = "date"
    INTERVAL = "interval"
    CRON = "cron"


class TimerMethod(enum.Enum):
    """
    SEND_MESSAGE - просто отправить смс
    """
    SEND_MESSAGE = "send_message"


class Timer(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=lambda: uuid.uuid4())
    name: str
    type: TimerType
    method: TimerMethod

    peer_id: typing.Optional[int]
    message_text: typing.Optional[str]
    message_attachment: typing.Optional[str]

    cron: typing.Optional[str]
    run_date: typing.Optional[datetime]
    interval: typing.Optional[int]

    @property
    def cron_params(self):
        """Gentool on https://ru.rakko.tools/tools/88/
        """
        return parse_cron_text(self.cron)

    @property
    def scheduler_params(self):
        data = {
            "id": self.id.hex,
            "name": "Таймер " + self.name,
            "trigger": self.type.value,
        }
        if self.type == TimerType.DATE:
            data['run_date'] = self.run_date
        elif self.type == TimerType.INTERVAL:
            data['seconds'] = self.interval
        else:
            data.update(**self.cron_params)
        return data
