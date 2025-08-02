"""
This module configures the BlackSheep application before it starts.
"""

import logging
from typing import Type

from blacksheep import Application
from rodi import ActivationScope, Container
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from increment.api.auth import configure_authentication
from increment.api.docs import configure_docs
from increment.api.errors import configure_error_handlers
from increment.api.services import configure_services
from increment.api.settings import Settings, load_settings
from increment.domain.models.increment import IncrementsCount
from increment.domain.repos.increment import IncrementRepo
from increment.domain.repos.increment_v2 import IncrementV2Repository
from increment.domain.services.increment import IncrementService
from increment.domain.services.increment_v2 import IncrementV2Service
from increment.infra.adapters.repos.increment import IncrementRepository
from increment.infra.adapters.repos.increment_v2 import (
    IncrementV2RepoAdapter as IncrementRepositoryV2Adapter,
)
from increment.infra.adapters.services.increment import (
    IncrementService as IncrementAdapter,
)
from increment.infra.adapters.services.increment_v2 import (
    IncrementServiceV2Adapter as IncrementV2Adapter,
)


def session_factory(
    scope: ActivationScope,
    activation_type: Type,
) -> AsyncSession:
    sm = scope.get(async_sessionmaker)

    return sm()


async def configure_sqlalchemy_engine(
    application: Application,
):
    logging.info("Configuring SQLAlchemy engine")
    settings = application.services.resolve(Settings)

    url = URL.create(
        drivername=settings.db_driver,
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )

    engine = create_async_engine(
        url,
    )
    async_session_maker = async_sessionmaker(
        expire_on_commit=False,
        class_=AsyncSession,
        bind=engine,
    )

    application.services.add_instance(
        engine,
    )

    application.services.add_instance(
        async_session_maker,
    )

    application.services.add_transient_by_factory(
        session_factory,
    )

    application.services.add_scoped(IncrementRepo, IncrementRepository)
    application.services.add_scoped(IncrementService, IncrementAdapter)

    srv = application.services.resolve(IncrementService)
    incr_count = await srv.get_count()

    application.services.add_instance(incr_count)

    # V2
    application.services.add_scoped(
        IncrementV2Service,
        IncrementV2Adapter,
    )
    application.services.add_scoped(
        IncrementV2Repository,
        IncrementRepositoryV2Adapter,
    )


async def configure_counter(
    application: Application,
):
    logging.info("Configuring global counter for V2 service.")
    srv = application.services.resolve(IncrementService)
    incr_count = await srv.get_count()

    application.services.register(IncrementsCount, incr_count)


async def dispose_sqlalchemy_engine(
    application: Application,
):
    logging.info("Disposing connection to SQLAlchemy engine")
    engine = application.services.resolve(AsyncEngine)

    await engine.dispose()


async def flush_counter(
    application: Application,
):
    logging.debug("Flushing increments counter")
    repo = application.services.resolve(IncrementV2Repository)
    await repo.flush_counter()


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    logging.basicConfig(level=settings.log_level)
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_docs(app, settings)

    app.on_start += configure_sqlalchemy_engine

    app.on_stop += flush_counter
    app.on_stop += dispose_sqlalchemy_engine

    return app


app = configure_application(*configure_services(load_settings()))
