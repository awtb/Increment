from blacksheep.server.controllers import APIController, get, post

from increment.domain.repos.increment import IncrementRepo
from increment.domain.services.increment import IncrementService


class IncrementController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def increment(self, increment_service: IncrementService):
        """
        Slower version of increment, v1
        """

        await increment_service.increment()

    @get()
    async def get_one(self, repo: IncrementRepo):
        return {"count": await repo.get_count()}


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
