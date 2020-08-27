import sys
import time


class Logger:
    def __getattr__(self, item):
        if item in ["remove", "add", "level"]:
            return lambda *args, **kwargs: None
        return Logger()

    def __call__(self, message: str):
        t = time.strftime("%m-%d %H:%M:%S", time.localtime())
        sys.stdout.write(
            "\n[IDM LP] "
            + str(message)
            + f" [TIME {t}]"
        )


try:
    from loguru import logger
except ImportError:
    logger = Logger()
