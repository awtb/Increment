"""
This module contains OpenAPI Documentation definition for the API.

It exposes a docs object that can be used to decorate request handlers with additional
information, used to generate OpenAPI documentation.
"""

from blacksheep import Application
from blacksheep.server.openapi.ui import ReDocUIProvider
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from increment.api.docs.binders import set_binders_docs
from increment.api.settings import Settings


def configure_docs(app: Application, settings: Settings):
    docs = OpenAPIHandler(
        info=Info(title=settings.info.title, version=settings.info.version),
        anonymous_access=True,
        ui_path="/swagger",
    )

    docs.ui_providers.append(
        ReDocUIProvider(
            ui_path="/docs",
        )
    )

    # include only endpoints whose path starts with "/api/"
    docs.include = lambda path, _: path.startswith("/api/")

    set_binders_docs(docs)

    docs.bind_app(app)
