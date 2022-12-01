import time

import requests
from loguru import logger

from red.config import config


def run():
    s = requests.Session()
    first = True
    while True:
        resp = s.get(f"http://{config.server_host}:{config.server_port}/process.php?")
        if first:
            logger.info(f"{resp}: {resp.text}")
            first = False
        time.sleep(1)
