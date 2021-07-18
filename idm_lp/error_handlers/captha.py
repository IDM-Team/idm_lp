from python_rucaptcha import ImageCaptcha
from vkbottle.exceptions import VKError
from vkbottle.framework.blueprint.user import Blueprint

from idm_lp.database import Database

user = Blueprint(
    name='captcha_error_blueprint'
)


@user.error_handler.captcha_handler
async def solve_captcha(e: VKError):
    db = Database.load()

    if not db.ru_captcha_key:
        return

    user_answer = ImageCaptcha. \
        ImageCaptcha(rucaptcha_key=db.ru_captcha_key). \
        captcha_handler(captcha_link=e.raw_error['captcha_img'])

    if not user_answer['error']:
        return user_answer['captchaSolve']
