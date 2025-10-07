from functools import lru_cache
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


env = os.getenv('ENV')
env_file = f'.env.{env}'

print(f'HASAn {env}')


class Setting(BaseSettings):
    NAME: str

    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')


@lru_cache
def get_settings():
    return Setting()  # type: ignore


settings = get_settings()
