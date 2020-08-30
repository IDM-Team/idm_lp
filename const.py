__version__ = '1.3.4'
__author__ = 'lordralinc'

DEFAULT_DATABASE = {
    "tokens": [],
    "secret_code": "",
    "ru_captcha_key": "",
    "delete_all_notify": False,
    "igrored_members": [],
    "igrored_global_members": [],
    "muted_members": [],
    "aliases": [],
    "service_prefixes": ["!слп", ".слп"],
    "self_prefixes": ["!л", ".л"],
    "duty_prefixes": ["!лд", ".лд"]
}

CONFIG_PATH = "config.json"
USE_APP_DATA = False

LOGGER_LEVEL = 'INFO'
VKBOTTLE_LOGGER_LEVEL = 'ERROR'
LOG_TO_PATH = False

CALLBACK_LINK = "https://irisduty.ru/callback/"

GITHUB_LINK = "https://github.com/LordRalInc/idmmulti_lp"
VERSION_REST = "https://raw.githubusercontent.com/LordRalInc/idmmulti_lp-rest/master/version.json"
ALIASES_REST = "https://raw.githubusercontent.com/LordRalInc/idmmulti_lp-rest/master/aliases.json"
ROLE_PLAY_COMMANDS_REST = "https://raw.githubusercontent.com/LordRalInc/idmmulti_lp-rest/master/role_play_commands.json"
