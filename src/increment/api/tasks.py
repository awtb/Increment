import asyncio
import logging

from rodi import Container

from increment.api.settings import Settings
from increment.domain.repos.counter import CounterRepo


async def flush_counter(container: Container) -> None:
    """Flushes the in-memory counter to the database."""
    logging.debug("Flushing increments counter")
    repo = container.resolve(CounterRepo)
    await repo.flush_counter()


async def flush_counter_periodically(container: Container) -> None:
    logging.info("Periodically flushing increments counter")
    settings = container.resolve(Settings)

    while True:
        logging.info("Flushing increments counter")
        try:
            await flush_counter(container)
        except Exception as e:
            logging.error(e)

        await asyncio.sleep(settings.counter_flush_interval)
