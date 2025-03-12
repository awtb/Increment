from abc import ABC, abstractmethod

from increment.domain.models.increment import IncrementsCount


class IncrementService(ABC):
    """Increment service"""

    @abstractmethod
    async def increment(self) -> None:
        """Increments inner record by one"""

        raise NotImplementedError

    @abstractmethod
    async def get_count(self) -> IncrementsCount:
        """Get count of increments"""

        raise NotImplementedError
