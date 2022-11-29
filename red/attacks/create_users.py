from red.config import config
from red.utils import client


def run():
    for user in config.our_users:
        client.create_user(user)
