from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from increment.domain.models.increment import IncrementsCount
from increment.domain.repos.increment_v2 import IncrementV2Repository
from increment.infra.adapters.repos.base import BaseRepo
from increment.infra.db.models import Increment


class IncrementV2RepoAdapter(IncrementV2Repository, BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self._initialized = False
        self._counter = 0
        self._update_interval = 100

    async def _initialize_counter(self):
        res = await self._session.execute(select(Increment).limit(1))
        incr_obj = res.scalars().first()
        self._counter = incr_obj.count
        self._initialized = True

    async def flush_counter(self):
        await self._session.execute(
            update(Increment).values(count=self._counter),
        )
        await self._session.commit()

    async def increment(self) -> None:
        if not self._initialized:
            await self._initialize_counter()

        self._counter += 1

        if self._counter % self._update_interval == 0:
            await self.flush_counter()

    async def get_count(self) -> IncrementsCount:
        if not self._initialized:
            await self._initialize_counter()

        return IncrementsCount(self._counter)
