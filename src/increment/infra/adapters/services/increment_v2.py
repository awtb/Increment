from increment.domain.models.increment import IncrementsCount
from increment.domain.repos.increment import IncrementRepo
from increment.domain.services.increment_v2 import IncrementV2Service


class IncrementServiceV2Adapter(IncrementV2Service):
    def __init__(self, increment_repo: IncrementRepo):
        super().__init__()
        self._increment_repo = increment_repo

    async def increment(self):
        await self._increment_repo.add_one()

    async def get_count(self) -> IncrementsCount:
        return await self._increment_repo.get_count()
