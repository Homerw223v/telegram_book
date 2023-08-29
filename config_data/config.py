from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    """Load variables from .env file
    :param path: Path to .env file
    :type path: str | None

    :rtype: Config
    :return: Class Config with all variables in .env file
    """
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        token=env('TOKEN'),
        admin_id=env.list('ADMIN')
    ))
