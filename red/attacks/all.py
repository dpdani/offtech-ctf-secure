from loguru import logger

from . import Attack

def run():
    for attack in Attack:
        if attack == Attack.all:
            continue
        logger.opt(ansi=True).info(f"<blue>Running {attack} attack.</blue>")
        Attack(attack).get_script().run()
