from fastapi import FastAPI
from src.campaign.configuration import Configuration
from src.campaign.controllers.campaign import register_campaign_router
from src.common.database.middleware import initialize_database_middleware
from src.common.health_checks.health_check import register_health_checks
from src.common.logger import initialize_logger
from src.common.context import initialize_context_middleware


def mock_health_check() -> bool:
    return True


def initialize_application(config: Configuration):
    initialize_logger(config.logging)
    application = FastAPI(
        title="Market Campaign API",
        version=config.version,
    )

    health_checks = [mock_health_check]

    # Middleware part
    initialize_context_middleware(application)
    # initialize_database_middleware(application, config.db, health_checks)

    # Router part
    register_campaign_router(application, "/v1")

    register_health_checks(application, health_checks)

    return application
