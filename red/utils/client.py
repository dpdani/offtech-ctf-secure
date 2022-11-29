from __future__ import annotations

from enum import Enum

import requests
from loguru import logger

from red.config import User, config


class Action(str, Enum):
    balance = "balance"
    register = "register"
    deposit = "deposit"
    withdraw = "withdraw"


def process(user: str | User = None, password: str = None, action: str = None, amount: str = None):
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
    logger.info(f"{url} -> {response}: {response.content}")
    return response


def create_user(user: User):
    return process(
        user=user,
        action=Action.register,
    )
