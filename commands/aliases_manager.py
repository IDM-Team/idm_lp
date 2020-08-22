import sys

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from objects import Database, Alias
from utils import edit_message

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
