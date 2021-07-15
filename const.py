import os
import json

__version__ = '1.10.0'
__author__ = 'lordralinc'

DEFAULT_DATABASE = {
  "tokens": [],
  "secret_code": "",
  "delete_all_notify": False,
  "ru_captcha_key": "",
  "ignored_members": [],
  "ignored_global_members": [],
  "muted_members": [],
  "aliases": [],
  "service_prefixes": [
    "!слп",
    ".слп"
  ],
  "self_prefixes": [
    "!л",
    ".л"
  ],
  "duty_prefixes": [
    "!лд",
    ".лд"
  ],
  "sloumo": [],
  "auto_exit_from_chat": False,
  "auto_exit_from_chat_delete_chat": False,
  "auto_exit_from_chat_add_to_black_list": False,
  "disable_notifications": False,
}

CONFIG_PATH = "config.json"
USE_APP_DATA = False

LOGGER_LEVEL = 'INFO'
VKBOTTLE_LOGGER_LEVEL = 'ERROR'
LOG_TO_PATH = False

CALLBACK_LINK = "https://irisduty.ru/callback/"

GITHUB_LINK = "https://github.com/lordralinc/idm_lp"
VERSION_REST = "https://raw.githubusercontent.com/lordralinc/idmmulti_lp-rest/master/version.json"
ALIASES_REST = "https://raw.githubusercontent.com/lordralinc/idmmulti_lp-rest/master/aliases.json"
ROLE_PLAY_COMMANDS_REST = "https://raw.githubusercontent.com/lordralinc/idmmulti_lp-rest/master/role_play_commands.json"
ROLE_PLAY_COMMANDS_USE_REST = True

ENABLE_EVAL = False
ALLOW_SENTRY = True
SENTRY_URL = "https://7a3f1b116c67453c91600ad54d4b7087@o481403.ingest.sentry.io/5529960"

with open(os.path.join(os.path.dirname(__file__), 'lp_dc_config.json'), 'r', encoding='utf-8') as file:
    data = json.loads(file.read())
    APP_ID = data.get('app_id', 0)
    APP_SECRET = data.get('app_secret', 0)


APP_USER_AGENT = f"IDMLP({APP_ID};{APP_SECRET})"