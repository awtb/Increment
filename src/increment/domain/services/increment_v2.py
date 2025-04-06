from abc import ABC, abstractmethod

from increment.domain.models.increment import IncrementsCount


class IncrementV2Service(ABC):
    """Increment version 2, faster version of Increment"""

    @abstractmethod
    async def increment(self) -> None:
        """Increments inner count by 1"""
        raise NotImplementedError()

    @abstractmethod
    async def get_count(self) -> IncrementsCount:
        """Returns inner counter"""
        raise NotImplementedError()
