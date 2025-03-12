from blacksheep.server.controllers import APIController, get, post

from increment.domain.models.increment import IncrementsCount
from increment.domain.services.increment import IncrementService


class IncrementController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def make_increment(self, increment_service: IncrementService):
        """
        Slower version of increment, v1
        """

        await increment_service.increment()

    @get()
    async def get_increments_count(
        self,
        service: IncrementService,
    ) -> IncrementsCount:
        """Get count of increments"""
        count = await service.get_count()

        return count


class IncrementControllerV2(APIController):
    @classmethod
    def version(cls) -> str:
        return "v2"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def increment(self):
        """
        Faster version of increment, v2
        """
