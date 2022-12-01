import time

from loguru import logger

from . import Attack

def run():
    for attack in Attack:
        if attack in [
            Attack.all,
            Attack.withdraw_all,
            Attack.gigi_is_ok,
            Attack.keep_very_alive,
            Attack.what_she_said,
            Attack.put_some,
        ]:
            continue
        logger.opt(ansi=True).info(f"<blue>Running {attack} attack.</blue>")
        Attack(attack).get_script().run()
        time.sleep(1)
    logger.info("Finished running attacks.")
