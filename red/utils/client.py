import re
from enum import Enum
from typing import Union

import requests
from loguru import logger

from red.config import User, config


class Action(str, Enum):
    balance = "balance"
    register = "register"
    deposit = "deposit"
    withdraw = "withdraw"


def process(user: Union[str, User] = None, password: str = None, action: str = None, amount: str = None):
    if isinstance(user, User):
        password = user.password
        user = user.user
    url = f"http://{config.server_host}:{config.server_port}/process.php?"
    if user is not None:
        url = f"{url}&user={user}"
    if password is not None:
        url = f"{url}&pass={password}"
    if action is not None:
        url = f"{url}&drop={action}"
    if amount is not None:
        url = f"{url}&amount={amount}"
    response = requests.get(url)
    logger.debug(f"{url} -> {response}: {response.content}")
    return response


def create_user(user: User):
    return process(
        user=user,
        action=Action.register,
    )

total_balance = re.compile(".*<td>Total</td><td>(\d+)</td>", re.DOTALL)

def get_balance(user: User):
    response = process(
        user=user,
        action=Action.balance,
    ).text
    try:
        balance = total_balance.match(response).groups()[0]
    except:
        logger.error(f"Could not read balance of {user}.")
        return None
    else:
        logger.info(f"{user} has balance {balance}")
        return int(balance)
