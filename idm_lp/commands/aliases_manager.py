from typing import List, Dict

import requests
from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp import const
from idm_lp.logger import logger, logger_decorator
from idm_lp.database import Database, Alias
from idm_lp.utils import edit_message

user = Blueprint(
    name='aliases_manager_blueprint'
)


def add_alias(database: Database, name: str, command_from: str, command_to: str) -> Alias:
    new_alias = Alias(**{
        'name': name,
        'command_from': command_from,
        'command_to': command_to
    })
    database.aliases.append(new_alias)
    database.save()
    return new_alias


def remove_alias(database: Database, alias: Alias) -> None:
    database.aliases.remove(alias)
    database.save()


def show_aliases(database: Database) -> str:
    if len(database.aliases):
        message = '📃 Ваши алиасы:\n'
        index = 1
        for alias in database.aliases:
            message += f"{index}. {alias.name} ({alias.command_from} -> !л {alias.command_to})\n"
            index += 1
        return message
    else:
        return "⚠ У вас нет алиасов"


def delete_last_space(value: str) -> str:
    if value[-1] == ' ':
        return value[:-1]
    return value


@user.on.message_handler(
    FromMe(),
    text="<prefix:service_prefix> +алиас <alias_name>\n<command_from>\n<command_to>"
)
@logger_decorator
async def add_alias_wrapper(message: Message, alias_name: str, command_from: str, command_to: str, *args, **kwargs):
    db = Database.get_current()
    logger.info(f"Создание алиаса\n")
    alias_name = delete_last_space(alias_name)
    command_from = delete_last_space(command_from)
    command_to = delete_last_space(command_to)

    for alias in db.aliases:
        if alias_name == alias.name:
            await edit_message(
                message,
                f"⚠ Алиас <<{alias_name}>> уже существует"
            )
            return

    new_alias = add_alias(db, alias_name, command_from, command_to)
    await edit_message(
        message,
        f"✅ Новый алиас <<{alias_name}>> создан\n"
        f"Команды: {new_alias.command_from} -> !л {command_to}"
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> алиасы")
@logger_decorator
async def show_aliases_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    logger.info(f"Просмотр алиасов\n")
    await edit_message(
        message,
        show_aliases(db)
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> -алиас <alias_name>")
@logger_decorator
async def remove_alias_wrapper(message: Message, alias_name: str, **kwargs):
    db = Database.get_current()
    logger.info(f"Удаление алиаса\n")
    alias_name = delete_last_space(alias_name)
    for alias in db.aliases:
        if alias_name == alias.name:
            remove_alias(db, alias)
            await edit_message(
                message,
                f"✅ Алиас <<{alias_name}>> удален"
            )
            return

    await edit_message(
        message,
        f'⚠ Алиас <<{alias_name}>> не найден'
    )


def get_alias_packs() -> Dict[str, List[Alias]]:
    data = requests.get(const.ALIASES_REST).json()
    packs = {}
    for key in data.keys():
        packs.update({
            key: [
                Alias(**dict_alias) for dict_alias in data[key]
            ]
        })
    return packs


def generate_aliases_pack_description(pack: List[Alias]) -> str:
    message = ""
    index = 1
    for alias in pack:
        message += f"{index}. {alias.name} ({alias.command_from} -> !л {alias.command_to})\n"
        index += 1
    return message


def check_name_duplicates(db: Database, pack: List[Alias]) -> bool:
    current_alias_names = [alias.name for alias in db.aliases]
    for alias in pack:
        if alias.name in current_alias_names:
            return False
    return True


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> алиасы импорт <pack_name>")
@logger_decorator
async def import_aliases_wrapper(message: Message, pack_name: str, **kwargs):
    db = Database.get_current()
    alias_packs = get_alias_packs()
    if pack_name not in alias_packs.keys():
        await edit_message(
            message,
            "⚠ Пак не найден"
        )
        return

    logger.info(f"Импорт алиасов\n")
    pack = alias_packs[pack_name]

    if not check_name_duplicates(db, pack):
        await edit_message(
            message,
            "⚠ Не удалось импортировать пак. Есть дубликаты."
        )
        return

    db.aliases.extend(pack)
    db.save()
    await edit_message(
        message,
        f"Импортированно {len(pack)} алиасов\n" + generate_aliases_pack_description(pack)
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> алиасы паки")
@logger_decorator
async def import_aliases_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    alias_packs = get_alias_packs()
    text = "📃 Паки алиасов:\n"
    index = 1
    for pack_name in alias_packs.keys():
        text += f"{index}. {pack_name} ({len(alias_packs[pack_name])} алиасов)\n"
        index += 1
    await edit_message(
        message,
        text
    )


@user.on.message_handler(FromMe(), text="<prefix:service_prefix> алиасы пак <pack_name>")
@logger_decorator
async def import_aliases_wrapper(message: Message, pack_name: str, **kwargs):
    db = Database.get_current()
    alias_packs = get_alias_packs()
    if pack_name not in alias_packs.keys():
        await edit_message(
            message,
            "⚠ Пак не найден"
        )
        return
    pack = alias_packs[pack_name]
    await edit_message(
        message,
        f"Пак алиасов <<{pack_name}>>:\n" +
        generate_aliases_pack_description(pack)
    )
