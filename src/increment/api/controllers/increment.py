from blacksheep.server.controllers import APIController, get, post

from increment.domain.repos.increment import IncrementRepo


class IncrementController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def increment(self, repo: IncrementRepo):
        """
        Slower version of increment, v1
        """

        await repo.add_one()

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
