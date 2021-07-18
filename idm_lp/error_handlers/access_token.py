from asyncio import sleep

from vkbottle.exceptions import VKError
from vkbottle.framework.blueprint.user import Blueprint

user = Blueprint(
    name='access_token_error_blueprint'
)


@user.error_handler.error_handler(5)
async def rps_handler(e: VKError):
    exit(1)
