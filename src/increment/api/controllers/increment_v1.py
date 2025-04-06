from blacksheep import JSONContent, Response
from blacksheep.server.controllers import APIController, get, post

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
    ) -> Response:
        """Get count of increments"""
        counter = await service.get_count()
        content = JSONContent(data={"count": counter.count})

        return Response(
            content=content,
            status=200,
        )
