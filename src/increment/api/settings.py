from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIInfo(BaseModel):
    title: str = "Increment API"
    version: str = "0.0.1"


class App(BaseModel):
    show_error_details: bool = False


class Site(BaseModel):
    copyright: str = "Example"


class Settings(BaseSettings):
    # to override info:
    # export app_info='{"title": "x", "version": "0.0.2"}'
    info: APIInfo = APIInfo()

    # to override api:
    # export app_app='{"show_error_details": True}'
    app: App = App()

    serving_host: str = Field(
        alias="SERVING_HOST",
        default="0.0.0.0",
    )

    serving_port: int = Field(
        alias="SERVING_PORT",
        default=8080,
    )

    db_driver: str = "postgresql+asyncpg"
    db_driver_sync: str = "postgresql+psycopg2"
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")


def load_settings() -> Settings:
    return Settings()
