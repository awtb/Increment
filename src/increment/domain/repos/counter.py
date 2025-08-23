import logging

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from increment.api.settings import Settings
from increment.domain.models.counter import Counter
from increment.domain.repos.base import BaseRepo
from increment.infra.db.models import Increment


class CounterRepo(BaseRepo):
    def __init__(
        self,
        settings: Settings,
        session: AsyncSession,
        increments_count: Counter,
    ) -> None:
        super().__init__(session)
        self._counter = increments_count
        self._update_interval = settings.counter_flush_interval
        self._logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    async def flush_counter(self) -> None:
        self._logger.info("Flushing increments counter")
        await self._session.execute(
            update(Increment).values(count=self._counter.count),
        )
        await self._session.commit()

    async def add_one(self) -> None:
        self._logger.debug(f"IncrementV2RepoAdapter.add_one: {self._counter}")

        self._counter.count += 1

        if self._counter.count % self._update_interval == 0:
            await self.flush_counter()

    async def get_counter(self) -> Counter:
        return self._counter
