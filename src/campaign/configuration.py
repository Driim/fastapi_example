import logging
from pydantic import BaseSettings
from src.common.database.configuration import DatabaseConfiguration

from src.common.logger.configuration import LoggerConfiguration


class Configuration(BaseSettings):
    logging: LoggerConfiguration = LoggerConfiguration()
    # db: DatabaseConfiguration = DatabaseConfiguration()
    version: str
