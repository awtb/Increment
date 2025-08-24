import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import URL, engine_from_config, pool


# Setup correct `$PYTHONPATH`, because our source files located at $PWD/src
src_path = Path(__file__).resolve().parent.parent  # это src
if src_path not in sys.path:
    sys.path.insert(0, str(src_path))


from alembic import context
from increment.api.settings import load_settings
from increment.infra.db.models import BaseModel

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = BaseModel.metadata

settings = load_settings()

url = URL.create(
    drivername=settings.db_driver_sync,
    username=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
    host=settings.db_host,
    port=settings.db_port,
)

config.set_main_option(
    "sqlalchemy.url",
    url.render_as_string(
        hide_password=False,
    ),
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
