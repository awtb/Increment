from abc import ABC, abstractmethod


class IncrementRepo(ABC):
    @abstractmethod
    async def add_one(self):
        """Adds one"""

        raise NotImplementedError

    async def get_count(self) -> int:
        """Get count"""

        raise NotImplementedError
