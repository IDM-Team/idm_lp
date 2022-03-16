from vkbottle.api import API

from idm_lp.database import Database, Timer


async def auto_infection_timer(api: API, db: Database):
    await api.messages.send(
        peer_id=db.auto_infection_peer_id,
        message=f"заразить {db.auto_infection_argument}",
        random_id=0,
    )


async def send_message_timer(api: API, db: Database, timer: Timer):
    await api.messages.send(
        peer_id=timer.peer_id,
        attachment=timer.message_attachment,
        message=timer.message_text,
        random_id=0
    )
