from typing import List, Optional

import tomlkit
from pydantic import BaseModel, BaseSettings


def read_conf_file(_: BaseSettings):
    with open("red-conf.toml", "rb") as f:
        return tomlkit.load(f)


class User(BaseModel):
    user: str
    password: str


class Attack(BaseModel):
    gateway_ext_ip: Optional[str] = None
    gateway_int_ip: Optional[str] = None
    spoof_blacklist: Optional[List[str]] = None
    clients: Optional[List[str]] = None


class Config(BaseSettings):
    server_host: str
    server_port: int
    attack: Attack = Attack()
    our_users: List[User]
    default_users: List[User]
    shared_users: List[User]

    class Config:
        env_prefix = 'RED_'

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            return (
                init_settings,
                read_conf_file,
                env_settings,
                file_secret_settings,
            )


config = Config()
