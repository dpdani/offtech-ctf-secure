from loguru import logger

from red.config import config
from red.utils import client


def run():
    for user in config.our_users:
        client.create_user(user)
        if client.get_balance(user) == 0:
            logger.info(f"{user} created.")
        else:
            logger.error(f"{user} not created.")
