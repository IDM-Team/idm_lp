from vkbottle.api import API

from idm_lp.database import Database


async def auto_infection_timer(api: API, db: Database):
    await api.messages.send(
        peer_id=db.auto_infection_peer_id,
        message=f"заразить {db.auto_infection_argument}",
        random_id=0,
    )
