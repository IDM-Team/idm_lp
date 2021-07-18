import sys
from idm_lp.main import run_lp
from idm_lp.setup import setup


if __name__ == "__main__":
    if 'setup' in sys.argv:
        setup()
        exit()
    run_lp()