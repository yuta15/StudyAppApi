from abc import ABC, abstractmethod
from uuid import UUID

from src.app.model.textbook import Chapter, Textbook, TextbookMetadata, TextbookSettings


class TextbookRepositoryInterface(ABC):
    @abstractmethod
    def save(self, textbook: Textbook) -> Textbook: ...

    @abstractmethod
    def get(self, textbook_id: UUID) -> Textbook: ...


class TextbookMetadataRepositoryInterface(ABC):
    @abstractmethod
    def save(self, metadata: TextbookMetadata) -> TextbookMetadata: ...

    @abstractmethod
    def get(self, textbook_id: UUID) -> TextbookMetadata: ...


class ChapterRepositoryInterface(ABC):
    @abstractmethod
    def save(self, chapter: Chapter) -> Chapter: ...

    @abstractmethod
    def get(self, chapter_id: UUID) -> Chapter: ...


class TextbookSettingsRepositoryInterface(ABC):
    @abstractmethod
    def save(self, textbook_settings: TextbookSettings) -> TextbookSettings: ...

    @abstractmethod
    def get(self, textbook_id: UUID) -> TextbookSettings: ...
