from abc import ABC, abstractmethod
from uuid import UUID

from src.app.service.interface.textbook.textbook_read_model import TextbookReadModel


class TextbookReadInterface(ABC):
    @abstractmethod
    def fetch_textbook(self, textbook_id: UUID) -> TextbookReadModel: ...
