import sys
from typing import List, Dict

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from objects import Database, Alias
from utils import edit_message

import requests
import const

user = Blueprint(
    name='aliases_manager_blueprint'
)


def add_alias(db: Database, name: str, command_from: str, command_to: str) -> Alias:
    new_alias = Alias({
        'name': name,
        'command_from': command_from,
        'command_to': command_to
    })
    db.aliases.append(new_alias)
    db.save()
    return new_alias


def remove_alias(db: Database, alias: Alias) -> None:
    db.aliases.remove(alias)
    db.save()


def show_aliases(db: Database) -> str:
    if len(db.aliases):
        message = '📃 Ваши алиасы:\n'
        index = 1
        for alias in db.aliases:
            message += f"{index}. {alias.name} ({alias.command_from} -> !л {alias.command_to})\n"
            index += 1
        return message
    else:
        return "⚠ У вас нет алиасов"


def delete_last_space(value: str) -> str:
    if value[-1] == ' ':
        return value[:-1]
    return value


@user.on.message(FromMe(), text="<prefix:service_prefix> +алиас <alias_name>\n<command_from>\n<command_to>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> +алиас <alias_name>\n<command_from>\n<command_to>")
async def add_alias_wrapper(message: Message, alias_name: str, command_from: str, command_to: str, **kwargs):
    sys.stdout.write(f"Создание алиаса\n")
    db = Database.load()
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


@user.on.message(FromMe(), text="<prefix:service_prefix> алиасы")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> алиасы")
async def show_aliases_wrapper(message: Message, **kwargs):
    sys.stdout.write(f"Просмотр алиасов\n")
    db = Database.load()
    await edit_message(
        message,
        show_aliases(db)
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> -алиас <alias_name>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> -алиас <alias_name>")
async def remove_alias_wrapper(message: Message, alias_name: str, **kwargs):
    sys.stdout.write(f"Удаление алиаса\n")
    db = Database.load()
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
                Alias(dict_alias) for dict_alias in data[key]
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


@user.on.message(FromMe(), text="<prefix:service_prefix> алиасы импорт <pack_name>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> алиасы импорт <pack_name>")
async def import_aliases_wrapper(message: Message, pack_name: str, **kwargs):
    alias_packs = get_alias_packs()
    if pack_name not in alias_packs.keys():
        await edit_message(
            message,
            "⚠ Пак не найден"
        )
        return

    sys.stdout.write(f"Импорт алиасов\n")
    pack = alias_packs[pack_name]

    db = Database.load()

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


@user.on.message(FromMe(), text="<prefix:service_prefix> алиасы паки")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> алиасы паки")
async def import_aliases_wrapper(message: Message, **kwargs):
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


@user.on.message(FromMe(), text="<prefix:service_prefix> алиасы пак <pack_name>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> алиасы пак <pack_name>")
async def import_aliases_wrapper(message: Message, pack_name: str, **kwargs):
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
