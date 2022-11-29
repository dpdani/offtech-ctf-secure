from red.config import config
from red.utils import client


INT_MAX = 2147483647


def run():
    user = config.our_users[0]
    client.process(
        user=user,
        action=client.Action.withdraw,
        amount=str(INT_MAX + 10),
    )
    client.process(
        user=user,
        action=client.Action.balance,
    )
