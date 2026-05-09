from abc import ABC, abstractmethod
from uuid import UUID


class TextbookAuthReadInterface(ABC):
    @abstractmethod
    def is_author(self, principal_id: UUID, textbook_id: UUID) -> bool: ...
