from asyncio import current_task
from contextlib import contextmanager
import json
import logging
from typing import ContextManager

from fastapi import Depends, FastAPI, status
import pydantic.json
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    AsyncSession,
)
from sqlalchemy.pool import NullPool

from src.common.context import get_request_context
from .configuration import DatabaseConfiguration

logger = logging.getLogger(__name__)


def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does
    """
    kwargs["default"] = pydantic.json.pydantic_encoder
    return json.dumps(*args, **kwargs)


# Why middleware?
# If we use Depends yield will return after response is send
class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    KEY = "session"

    def __init__(self, config: DatabaseConfiguration, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._engine = create_async_engine(
            config.url,
            echo=config.echo,
            echo_pool=config.echo,
            future=True,
            # NullPool used because we have Odyssey in front of PostgreSQL
            # in another case SQLAlchemy will try to save prepared statements
            poolclass=NullPool,
            json_serializer=_custom_json_serializer,
            connect_args={"ssl": config.use_ssl},
        )
        self._session_factory = async_scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )

    @contextmanager
    def _session_manager(self) -> ContextManager[AsyncSession]:
        session = self._session_factory()
        context = get_request_context()
        context[self.KEY] = session

        try:
            yield session
        finally:
            del context[self.KEY]

    async def dispatch(
        self, request: Request, next: RequestResponseEndpoint
    ) -> Response:
        with self._session_manager as session:
            try:
                response = await next(request)
                code = response.status_code

                if code and code < status.HTTP_400_BAD_REQUEST:
                    await session.commit()
                else:
                    logger.info(f"Bad response status({code}), rollback")
                    await session.rollback()
            except Exception as exc:
                await session.rollback()
                raise exc
            finally:
                await session.close()

            return response


def get_session() -> AsyncSession:
    context = get_request_context()
    # we want to raise error if KEY not in context
    return context[DatabaseSessionMiddleware.KEY]


async def check_database_connection(
    session: AsyncSession = Depends(get_session),
) -> bool:
    try:
        await session.execute("SELECT 1")
        return True
    except:  # noqa
        logger.error("READINESS: database connection")
        return False


def initialize_database_middleware(
    application: FastAPI, config: DatabaseConfiguration, health_checks: list
) -> None:
    application.add_middleware(DatabaseSessionMiddleware, config=config)
    health_checks.append(check_database_connection)
