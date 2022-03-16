import re

from collections import namedtuple
from typing import Optional, NamedTuple

from vkbottle.user import Blueprint, Message
from vkbottle.rule import FromMe

from idm_lp import rules
from idm_lp.logger import logger_decorator
from idm_lp.database import Database
from idm_lp.utils import edit_message

user = Blueprint(
    name='bio_wars_blueprint'
)

RegexFindAllBase = namedtuple('RegexFindAll', ['regex', 'groups_map'])


class RegexFindAll(RegexFindAllBase):

    def match(self, text: str) -> Optional[NamedTuple]:
        re_result = re.findall(self.regex, text)
        if re_result:
            if isinstance(re_result[0], tuple):
                return namedtuple('RegexFindAllResult', self.groups_map)(*[str(res) for res in re_result[0]])
            else:
                return namedtuple('RegexFindAllResult', self.groups_map)(str(re_result[0]))
        return None


USER_ID_REGEX = RegexFindAll(
    re.compile(
        r'Организатор заражения: \[id(?P<user_id>\d+)',
        flags=re.MULTILINE & re.IGNORECASE
    ),
    ['user_id']
)


@user.on.message_handler(rules.ContainsRule(['Служба безопасности лаборатории']))
@logger_decorator
async def bio_reply_handler(message: Message):
    if message.from_id > 0:
        return

    db = Database.get_current()
    if not db.bio_reply:
        return

    if str(await message.api.user_id) not in message.text:
        return

    lab_user = USER_ID_REGEX.match(message.text)
    if lab_user:
        # noinspection PyUnresolvedReferences
        return f"Заразить @id{lab_user.user_id}"


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -заражение")
@logger_decorator
async def activate_bio_reply_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.bio_reply = False
    db.save()
    await edit_message(
        message,
        "✅ Заражение в ответ отключено"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> +заражение")
@logger_decorator
async def deactivate_bio_reply_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    db.bio_reply = True
    db.save()
    await edit_message(
        message,
        "✅ Заражение в ответ включено"
    )
