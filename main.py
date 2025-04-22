import os

from loguru import logger

from settings.settings import Settings
from src.user.user import User
from src.utils.utils import load_accounts

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_PATH = os.path.join(ROOT_DIR, 'config/account.json')

if __name__ == '__main__':
    settings = Settings(root_dir=ROOT_DIR)
    user = User(settings=settings)

    try:
        accounts = load_accounts(ACCOUNTS_PATH)
        for account in accounts:
            user.run_actions(account)
    except Exception as e:
        logger.error(f"❌ Error loading account information: {e}")



