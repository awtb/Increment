from blacksheep.server.controllers import APIController, get, post

from increment.domain.models.increment import IncrementsCount
from increment.domain.services.increment_v2 import IncrementV2Service


class IncrementControllerV2(APIController):
    @classmethod
    def version(cls) -> str:
        return "v2"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def make_increment(self, increment_service: IncrementV2Service):
        """
        Faster version of increment, v2
        """

        await increment_service.increment()

    @get()
    async def get_increments_count(
        self,
        service: IncrementV2Service,
    ) -> IncrementsCount:
        """Get count of increments, v2"""
        count = await service.get_count()

        return count
