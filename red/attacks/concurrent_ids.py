import threading

from red.config import User
from red.utils import client


def run():
    user1 = User(user="whoami", password="whoami")
    user2 = User(user="whoami", password="whoami2")
    threads = [
        threading.Thread(target=client.create_user, args=(user1,)),
        threading.Thread(target=client.create_user, args=(user2,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
