from increment.domain.repos.counter import Counter, CounterRepo


class CounterService:
    def __init__(self, counter_repo: CounterRepo) -> None:
        super().__init__()
        self._counter_repo = counter_repo

    async def increment(self) -> None:
        await self._counter_repo.add_one()

    async def get_count(self) -> Counter:
        return await self._counter_repo.get_counter()
