import json
import time

from loguru import logger

from red.utils import client


with open("./red/blns.json", 'rb') as f:
    blns = json.load(f)


def run():
    logger.info(blns)
    logger.info(f"Found {len(blns)} naughty strings.")
    for string in blns:
        client.process(
            user=string,
            password=string,
            action=string,
            amount=string,
        )
        time.sleep(1)
    for string in blns:
        for action in client.Action:
            client.process(
                user=string,
                password=string,
                action=action,
                amount=string,
            )
            time.sleep(1)
