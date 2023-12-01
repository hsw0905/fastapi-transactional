import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "local"
    DEBUG: bool = True

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    DB_URL: str = f"sqlite:///:memory:"
    DB_ECHO: bool = True
    DB_PRE_PING: bool = True


class DevelopmentConfig(Config):
    ENV: str = "development"
    DB_URL: str = os.getenv("DB_URL", f"sqlite:///:memory:")


class LocalConfig(Config):
    DB_URL: str = os.getenv("DB_URL", f"sqlite:///:memory:")


class TestConfig(Config):
    ENV: str = "test"


class ProductionConfig(Config):
    ENV: str = "production"
    DEBUG: bool = False
    DB_URL: str = os.getenv("DB_URL", f"sqlite:///:memory:")
    DB_ECHO: bool = False


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config = get_config()
