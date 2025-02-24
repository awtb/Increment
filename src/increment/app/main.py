"""
This module configures the BlackSheep application before it starts.
"""

from blacksheep import Application
from rodi import Container

from increment.app.auth import configure_authentication
from increment.app.docs import configure_docs
from increment.app.errors import configure_error_handlers
from increment.app.services import configure_services
from increment.app.settings import load_settings, Settings


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
    return app


app = configure_application(*configure_services(load_settings()))
