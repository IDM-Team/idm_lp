from typing import Dict, Any, List

from objects.base import BaseModel


class TrustedUser(BaseModel):
    user_id: int

    def save(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id
        }
