from sqlalchemy import select, update

from increment.domain.models.increment import IncrementsCount
from increment.domain.repos.increment import IncrementRepo
from increment.infra.adapters.repos.base import BaseRepo
from increment.infra.db.models import Increment


class IncrementRepository(IncrementRepo, BaseRepo):
    async def get_count(self) -> IncrementsCount:
        res = await self._session.execute(select(Increment))

        incr_obj = res.scalars().first()

        return IncrementsCount(count=incr_obj.count)  # type: ignore

    async def add_one(self):
        await self._session.execute(
            update(Increment).values(count=Increment.count + 1),
        )

        await self._session.commit()
