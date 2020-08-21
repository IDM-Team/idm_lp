from asyncio import sleep

from vkbottle.exceptions import VKError
from vkbottle.framework.blueprint.user import Blueprint

user = Blueprint(
    name='rps_error_blueprint'
)


@user.error_handler.error_handler(6)
async def rps_handler(e: VKError):
    await sleep(1)
    return await e.method_requested(**e.params_requested)
