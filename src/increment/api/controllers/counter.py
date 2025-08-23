from blacksheep.server.controllers import APIController, get, post

from increment.domain.models.counter import Counter
from increment.domain.services.counter import CounterService


class CounterController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "counter"

    @post()
    async def increment(
        self,
        increment_service: CounterService,
    ) -> None:
        """
        Increment inner counter
        """

        await increment_service.increment()

    @get()
    async def get_counter(
        self,
        increments_count: Counter,
    ) -> Counter:
        """
        Get current increments count
        """
        return increments_count
