from abc import abstractmethod, ABC
from typing import Dict, Any

from objects.dotdict import DotDict


class BaseModel(ABC, DotDict):

    @abstractmethod
    def save(self) -> Dict[str, Any]:
        ...
