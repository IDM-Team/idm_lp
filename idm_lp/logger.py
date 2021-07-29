import sys
import time
from typing import Callable, Union

from vkbottle import Message


class LoggerLevel:
    levels = {
        'debug': 0,
        'info': 1,
        "warning": 2,
        "warn": 2,
        "error": 3,
        "critical": 4,
        "crit": 4,
    }

    @staticmethod
    def get_int(level: Union[int, str]) -> int:
        if isinstance(level, int):
            return level

        return LoggerLevel.levels[level.lower()]

    @staticmethod
    def get_name(level: int) -> str:
        for key in LoggerLevel.levels.keys():
            if LoggerLevel.levels[key] == level:
                return key
        return "unknown"

    @staticmethod
    def get_cap_name(level: int) -> str:
        return LoggerLevel.get_name(level).upper()

    @staticmethod
    def get_short_name(level: int) -> str:
        return LoggerLevel.get_cap_name(level)[0]


class Logger(object):

    global_logger_level = 1

    def __init__(self, level: Union[int, str] = 1):
        self.logger_level = LoggerLevel.get_int(level)

    def __getattr__(self, item):
        if item in ["remove", "add", "level"]:
            return lambda *args, **kwargs: None

        if item in LoggerLevel.levels.keys():
            new_logger = Logger(LoggerLevel.get_int(item))
            new_logger.global_logger_level = self.global_logger_level
            return new_logger

        return super(Logger, self).__getattr__(item)

    def __call__(self, message: str, *args, **kwargs):
        if self.logger_level < self.global_logger_level:
            return

        output = sys.stdout if self.logger_level < 3 else sys.stderr
        t = time.strftime("%m-%d %H:%M:%S", time.localtime())

        try:
            message = str(message).format(*args, **kwargs)
        except:
            message = f"{message} {args} {kwargs}"

        output.write(
            f"\n[IDM LP] | {LoggerLevel.get_short_name(self.logger_level)} | "
            + message
            + f" [TIME {t}]"
        )


try:
    from loguru import logger
except ImportError:
    logger = Logger()


def logger_decorator(func: Callable) -> Callable:
    async def decorator(message: Message, *args, **kwargs):
        global logger
        try:
            start = time.time()
            result = await func(message, *args, **kwargs)
            delta = round(time.time() - start, 4)
            text = f"Message {message.id} ({message.peer_id}/{message.from_id}) " \
                   f"handled with function «{func.__name__}». " \
                   f"Text: «{message.text}». " \
                   f"Result: {result}. " \
                   f"Delta: {delta}"
            logger.info(text)
            return result
        except Exception as ex:
            text = f"Message {message.id} ({message.peer_id}/{message.from_id}) " \
                   f"handled with function «{func.__name__}». " \
                   f"Text: «{message.text}». " \
                   f"Error: {ex}."
            logger.error(text)

    return decorator
