"""
This module configures the BlackSheep application before it starts.
"""

import asyncio
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
from increment.api.tasks import flush_counter, flush_counter_periodically
from increment.domain.models.counter import Counter
from increment.domain.repos.counter import CounterRepo
from increment.domain.services.counter import CounterService


async def counter_factory(container: Container) -> Counter:
    """Creates an in-memory counter initialized from the repository."""
    repo = CounterRepo(
        settings=container.resolve(Settings),
        session=container.resolve(AsyncSession),
        global_counter=Counter(count=0),
    )
    current_counter = await repo.get_counter()
    return Counter(count=current_counter.count)


def session_factory(
    scope: ActivationScope,
    activation_type: Type,
) -> AsyncSession:
    """Provides a new AsyncSession from the async_sessionmaker."""
    return scope.get(async_sessionmaker)()


async def configure_sqlalchemy(application: Application) -> None:
    """Configures SQLAlchemy engine and session factory."""
    logging.info("Configuring SQLAlchemy engine")
    settings = application.services.resolve(Settings)

    engine = create_async_engine(
        URL.create(
            drivername=settings.db_driver,
            username=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
        ),
    )

    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    services = application.services
    services.add_instance(engine)
    services.add_instance(session_maker)
    services.add_transient_by_factory(session_factory)


async def configure_app_services(application: Application) -> None:
    """Configures domain repositories and services."""
    services = application.services

    counter = await counter_factory(services)
    services.add_instance(counter)
    services.add_scoped(CounterRepo, CounterRepo)
    services.add_scoped(CounterService, CounterService)


async def dispose_sqlalchemy(application: Application) -> None:
    """Disposes the SQLAlchemy engine on shutdown."""
    logging.info("Disposing SQLAlchemy engine")
    engine = application.services.resolve(AsyncEngine)
    await engine.dispose()


async def configure_background_tasks(application: Application) -> None:
    """Configures background tasks"""
    asyncio.create_task(
        flush_counter_periodically(application.services),
    )


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    """Sets up the BlackSheep application with all required components."""
    logging.basicConfig(level=settings.log_level)
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_docs(app, settings)

    app.on_start += configure_sqlalchemy
    app.on_start += configure_app_services
    app.on_start += configure_background_tasks
    app.on_stop += flush_counter
    app.on_stop += dispose_sqlalchemy

    return app


app = configure_application(*configure_services(load_settings()))
