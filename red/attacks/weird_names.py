import time

from red.config import User
from red.utils import client


names = [
    "👻asdasdasd",
    "asd👻asdasd",
    "asdasdasd👻",
    "asdasdasd\0",
    "asdasdasdd\b",
    "asdasdas\0d",
    "asdasdasd\rasdasdasd",
    "asdasdasd\rasdasdasd",
]
names.extend([
    f"asdasdasd{chr(c)}" for c in range(300)
])

def run():
    for name in names:
        u = User(user=name, password="myuserpassword")
        client.create_user(u)
        if client.get_balance(u) is not None:
            client.create_user(User(user=name, password="myduplicatepassw"))
        # time.sleep(0.3)
