from red.config import User, config
from red.utils import client


def withdraw_all_for(user: User):
    balance = client.process(user=user, action=client.Action.balance)
    client.process(user=user, action=client.Action.withdraw, amount=balance)


def run():
    for user in config.our_users:
        withdraw_all_for(user)
