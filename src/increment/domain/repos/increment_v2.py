from abc import ABC, abstractmethod

from increment.domain.models.increment import IncrementsCount


class IncrementV2Repository(ABC):
    @abstractmethod
    async def add_one(self) -> None:
        """Increments inner count by 1"""
        raise NotImplementedError

    @abstractmethod
    async def get_count(self) -> IncrementsCount:
        """Increments inner count by 1"""
        raise NotImplementedError

    @abstractmethod
    async def flush_counter(self) -> None:
        raise NotImplementedError
