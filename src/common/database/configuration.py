from pydantic import BaseSettings


class DatabaseConfiguration(BaseSettings):
    url: str
    echo: bool = False
    use_ssl: bool = True

    class Config:
        env_prefix = "db_"
