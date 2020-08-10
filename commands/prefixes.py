import sys

from vkbottle.rule import FromMe
from vkbottle.user import Blueprint, Message

from objects import Database
from utils import edit_message

user = Blueprint(
    name='prefixes_blueprint'
)


def show_self_prefixes(db: Database) -> str:
    index = 1
    message = '📃 Ваши префиксы для собственных сигналов\n'
    for prefix in db.self_prefixes:
        message += f'{index}. {prefix}\n'
        index += 1
    return message


def show_duty_prefixes(db: Database) -> str:
    index = 1
    message = '📃 Ваши префиксы для сигналов дежурному\n'
    for prefix in db.duty_prefixes:
        message += f'{index}. {prefix}\n'
        index += 1
    return message


def add_self_prefix(db: Database, prefix: str) -> None:
    db.self_prefixes.append(prefix)
    db.save()


def add_duty_prefix(db: Database, prefix: str) -> None:
    db.duty_prefixes.append(prefix)
    db.save()


def remove_self_prefix(db: Database, prefix: str) -> None:
    db.self_prefixes.remove(prefix)
    db.save()


def remove_duty_prefix(db: Database, prefix: str) -> None:
    db.duty_prefixes.remove(prefix)
    db.save()


@user.on.message(FromMe(), text="<prefix:service_prefix> префиксы свои")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> префиксы свои")
async def show_self_prefixes_wrapper(message: Message, **kwargs):
    sys.stdout.write(f'Просмотр своих префиксов\n')
    db = Database.load()
    await edit_message(
        message,
        show_self_prefixes(db)
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> префиксы дежурный")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> префиксы дежурный")
async def show_duty_prefixes_wrapper(message: Message, **kwargs):
    sys.stdout.write(f'Просмотр префиксов дежурного\n')
    db = Database.load()
    await edit_message(
        message,
        show_duty_prefixes(db)
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> +префикс свой <new_prefix>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> +префикс свой <new_prefix>")
async def add_self_prefix_wrapper(message: Message, new_prefix: str, **kwargs):
    sys.stdout.write(f'Создание своего префикса\n')
    db = Database.load()
    new_prefix = new_prefix.replace(' ', '')
    if new_prefix in db.self_prefixes:
        await edit_message(
            message,
            f'⚠ Префикс <<{new_prefix}>> уже существует'
        )
        return
    add_self_prefix(db, new_prefix)
    await edit_message(
        message,
        f'✅ Новый префикс <<{new_prefix}>> создан'
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> +префикс дежурный <new_prefix>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> +префикс дежурный <new_prefix>")
async def add_duty_prefix_wrapper(message: Message, new_prefix: str, **kwargs):
    sys.stdout.write(f'Создание префикса дежурного\n')
    db = Database.load()
    new_prefix = new_prefix.replace(' ', '')
    if new_prefix in db.duty_prefixes:
        await edit_message(
            message,
            f'⚠ Префикс <<{new_prefix}>> уже существует'
        )
        return
    add_duty_prefix(db, new_prefix)
    await edit_message(
        message,
        f'✅ Новый префикс <<{new_prefix}>> создан'
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> -префикс свой <old_prefix>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> -префикс свой <old_prefix>")
async def remove_self_prefix_wrapper(message: Message, old_prefix: str, **kwargs):
    sys.stdout.write(f'Удаление своего префикса\n')
    db = Database.load()
    old_prefix = old_prefix.replace(' ', '')
    if old_prefix not in db.self_prefixes:
        await edit_message(
            message,
            f'⚠ Префикса <<{old_prefix}>> не существует'
        )
        return
    remove_self_prefix(db, old_prefix)
    await edit_message(
        message,
        f'✅ Префикс <<{old_prefix}>> удален'
    )


@user.on.message(FromMe(), text="<prefix:service_prefix> -префикс дежурный <old_prefix>")
@user.on.chat_message(FromMe(), text="<prefix:service_prefix> -префикс дежурный <old_prefix>")
async def remove_duty_prefix_wrapper(message: Message, old_prefix: str, **kwargs):
    sys.stdout.write(f'Удаление префикса дежурного\n')
    db = Database.load()
    old_prefix = old_prefix.replace(' ', '')
    if old_prefix not in db.duty_prefixes:
        await edit_message(
            message,
            f'⚠ Префикса <<{old_prefix}>> не существует'
        )
        return
    remove_duty_prefix(db, old_prefix)
    await edit_message(
        message,
        f'✅ Префикс <<{old_prefix}>> удален'
    )
