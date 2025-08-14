from increment.api.schemas.count import IncrementsCount
from increment.domain.repos.increment import IncrementRepo
from increment.domain.services.increment import (
    IncrementService as AbstractIncrementService,
)


class IncrementService(AbstractIncrementService):
    """Adapter for `AbstractIncrementService`"""

    def __init__(
        self,
        increment_repo: IncrementRepo,
    ) -> None:
        self._increment_repo = increment_repo

    async def get_count(self) -> IncrementsCount:
        count = await self._increment_repo.get_count()
        return count

    async def increment(self) -> None:
        await self._increment_repo.add_one()
