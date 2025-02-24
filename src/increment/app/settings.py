"""
Application settings handled using Pydantic Settings management.

Pydantic is used both to read app settings from various sources, and to validate their
values.

https://docs.pydantic.dev/latest/usage/settings/
"""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIInfo(BaseModel):
    title: str = "Increment API"
    version: str = "0.0.1"


class App(BaseModel):
    show_error_details: bool = False


class Site(BaseModel):
    copyright: str = "Example"


class Serving(BaseModel):
    port: int = Field(default=8000, alias="SERVING_PORT")
    host: str = Field(default="0.0.0.0", alias="SERVING_HOST")


class Settings(BaseSettings):
    # to override info:
    # export app_info='{"title": "x", "version": "0.0.2"}'
    info: APIInfo = APIInfo()

    # to override app:
    # export app_app='{"show_error_details": True}'
    app: App = App()

    serving: Serving = Serving()

    model_config = SettingsConfigDict(env_prefix="APP_")


def load_settings() -> Settings:
    return Settings()
