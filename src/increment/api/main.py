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
from increment.domain.models.counter import Counter
from increment.domain.repos.counter import CounterRepo
from increment.domain.services.counter import CounterService


async def counter_factory(container: Container) -> Counter:
    repository = CounterRepo(
        settings=container.resolve(Settings),
        session=container.resolve(AsyncSession),
        increments_count=Counter(count=0),
    )
    counter = await repository.get_counter()
    return Counter(count=counter.count)


def session_factory(
    scope: ActivationScope,
    activation_type: Type,
) -> AsyncSession:
    sm = scope.get(async_sessionmaker)

    return sm()


async def configure_sqlalchemy_engine(
    application: Application,
) -> None:
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

    counter = await counter_factory(application.services)

    application.services.add_instance(
        counter,
    )

    application.services.add_scoped(
        CounterRepo,
        CounterRepo,
    )

    application.services.add_scoped(
        CounterService,
        CounterService,
    )


async def configure_counter(
    application: Application,
) -> None:
    logging.info("Configuring global counter for V2 service.")
    srv = application.services.resolve(CounterService)
    incr_count = await srv.get_count()

    application.services.register(Counter, incr_count)


async def dispose_sqlalchemy_engine(
    application: Application,
) -> None:
    logging.info("Disposing connection to SQLAlchemy engine")
    engine = application.services.resolve(AsyncEngine)

    await engine.dispose()


async def flush_counter(
    application: Application,
) -> None:
    logging.debug("Flushing increments counter")
    repo = application.services.resolve(CounterRepo)
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
