from red.config import config
from red.utils import client


def run():
    for user in config.our_users:
        client.process(user, action=client.Action.deposit, amount='10')
        client.get_balance(user)
