import time

from red.config import config
from red.utils import client


def run():
    while True:
        client.get_balance(config.our_users[0])
        time.sleep(1)
