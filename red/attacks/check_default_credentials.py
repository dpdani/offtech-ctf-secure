from red.config import User, config
from red.utils import client


def check_credentials(user: User):
    response = client.process(user, client.Action.balance)
    response = client.process(user.user, user.password + "\0aaaaaaaaa", client.Action.balance)


def run():
    for user in config.default_users:
        check_credentials(user)
