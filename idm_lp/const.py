import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler


__version__ = '1.13.3'
__author__ = 'lordralinc'
__description__ = (
    "LP модуль позволяет работать приемнику сигналов «IDM multi» работать в любых чатах. "
    "Так же он добавляет игнор, глоигнор, мут и алиасы."
)

CONFIG_PATH = "config.json"
USE_APP_DATA = False

LOGGER_LEVEL = 'INFO'
VKBOTTLE_LOGGER_LEVEL = 'ERROR'
LOG_TO_PATH = False

BASE_DOMAIN = "https://idmduty.ru"


def CALLBACK_LINK():
    return f"{BASE_DOMAIN}/callback/"


def GET_LP_INFO_LINK():
    return f"{BASE_DOMAIN}/api/dutys/get_lp_info/"

def SAVE_LP_INFO_LINK():
    return f"{BASE_DOMAIN}/api/dutys/save_lp_info/"

GITHUB_LINK = "https://github.com/IDM-Team/idm_lp"
VERSION_REST = "https://raw.githubusercontent.com/IDM-Team/idm_lp/master/rest/version.json"
ALIASES_REST = "https://raw.githubusercontent.com/IDM-Team/idm_lp/master/rest/aliases.json"
ROLE_PLAY_COMMANDS_REST = "https://raw.githubusercontent.com/IDM-Team/idm_lp/master/rest/role_play_commands.json"

ENABLE_EVAL = False
ALLOW_SENTRY = True

try:
    with open('lp_dc_config.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
        APP_ID = data.get('app_id', 0)
        APP_SECRET = data.get('app_secret', "public")
except:
    APP_ID = 0
    APP_SECRET = "public"

APP_USER_AGENT = f"IDMLP({APP_ID};{APP_SECRET})"


scheduler = AsyncIOScheduler()
