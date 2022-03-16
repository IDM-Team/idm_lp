import logging

from idm_lp.main import run_lp

logging.getLogger('apscheduler').setLevel(logging.DEBUG)


if __name__ == "__main__":
    run_lp()
