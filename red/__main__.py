import socket
import sys
from typing import Optional

import typer
from loguru import logger

from red.attacks import Attack
from red.config import config
from red.utils import get_experiment_interface_and_ip


cli = typer.Typer()

interface, ip = get_experiment_interface_and_ip()
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    f"<cyan>{ip} {interface} {socket.gethostname().split('.')[0]}</cyan> | "
    "<level>{message}</level>"
)
logger.configure(extra={"ip": "", "user": ""})  # Default values
logger.remove()
logger.add(sys.stdout, format=logger_format)


def error(message):
    typer.secho(message, fg='red')


@cli.command()
def attack(attack_name: Attack):
    logger.info(f"Using config: {config}")
    script = attack_name.get_script()
    if script is None:
        error(f"Script named '{attack_name}' not found.")
        return 2
    script.run()


if __name__ == '__main__':
    cli()
