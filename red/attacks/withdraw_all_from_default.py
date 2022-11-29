from red.attacks.withdraw_all import withdraw_all_for
from red.config import config


def run():
    for user in config.default_users:
        withdraw_all_for(user)
