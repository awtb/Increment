"""
This module configures the BlackSheep application before it starts.
"""

from typing import Type

from blacksheep import Application
from rodi import ActivationScope, Container
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from increment.app.auth import configure_authentication
from increment.app.docs import configure_docs
from increment.app.errors import configure_error_handlers
from increment.app.services import configure_services
from increment.app.settings import Settings, load_settings


def session_factory(
    scope: ActivationScope,
    activation_type: Type,
) -> AsyncSession:
    sm = scope.get(async_sessionmaker)

    return sm()


async def configure_sqlalchemy_engine(
    application: Application,
):
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


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_docs(app, settings)

    app.on_start += configure_sqlalchemy_engine

    return app


app = configure_application(*configure_services(load_settings()))
