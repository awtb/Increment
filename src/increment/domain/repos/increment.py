from abc import ABC, abstractmethod

from increment.api.schemas.count import IncrementsCount


class IncrementRepo(ABC):
    @abstractmethod
    async def add_one(self) -> None:
        """Adds one"""

        raise NotImplementedError

    @abstractmethod
    async def get_count(self) -> IncrementsCount:
        """Get count"""

        raise NotImplementedError
