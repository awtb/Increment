from abc import ABC, abstractmethod


class IncrementV2Service(ABC):
    """Increment version 2, faster version of Increment"""

    @abstractmethod
    async def increment(self) -> None:
        """Increments inner count by 1"""
        raise NotImplementedError()

    @abstractmethod
    async def get_count(self) -> int:
        """Returns inner counter"""
        raise NotImplementedError()
