import threading
import time

from red.config import User
from red.utils import client


def attempt(i):
    user1 = User(user=f"whoami{i}", password="asdasdwhoami")
    user2 = User(user=f"whoami{i}", password="asdasdwhoami2")
    threads = [
        threading.Thread(target=client.create_user, args=(user1,)),
        threading.Thread(target=client.create_user, args=(user2,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run():
    i = 0
    while True:
        attempt(i)
        time.sleep(1)
        i += 1
