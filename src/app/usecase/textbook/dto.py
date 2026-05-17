from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

from src.app.model.textbook import TextbookStatus, TitleString


@dataclass
class CreateTextbookDTO:
    principal_id: UUID
    title: TitleString


@dataclass
class TextbookDTO:
    principal_id: UUID | None
    textbook_id: UUID


@dataclass
class GetChapterDTO:
    principal_id: UUID
    textbook_id: UUID
    chapter_id: UUID


@dataclass
class ModifyTextbookDTO:
    principal_id: UUID
    textbook_id: UUID
    title: TitleString | None = None
    status: TextbookStatus | None = None


@dataclass
class OutputTextbookMetadata:
    created_at: datetime
    updated_at: datetime


@dataclass
class OutputTextbookModified:
    textbook_id: UUID
    title: TitleString
    status: TextbookStatus
    metadata: OutputTextbookMetadata


@dataclass
class ChapterDTO:
    chapter_id: UUID
    title: TitleString | None
    content: str


@dataclass
class AuthorTextbookDTO:
    principal_id: UUID
    textbook_id: UUID
    author_id: UUID


@dataclass
class AddChapterDTO:
    principal_id: UUID
    textbook_id: UUID
    chapter_title: TitleString


@dataclass
class RemoveChapterDTO:
    principal_id: UUID
    textbook_id: UUID
    chapter_id: UUID


@dataclass
class ReorderChaptersDTO:
    principal_id: UUID
    textbook_id: UUID
    chapter_ids: list[UUID]


@dataclass
class ModifyChapterDTO:
    principal_id: UUID
    textbook_id: UUID
    chapter_id: UUID
    title: TitleString | None = None
    content: str | None = None


@dataclass
class TextbookSettingsDTO:
    is_public: bool


@dataclass
class GetTextbookSettingsOutputDTO:
    textbook_id: UUID
    settings: TextbookSettingsDTO


@dataclass
class ModifyTextbookSettingsDTO:
    principal_id: UUID
    textbook_id: UUID
    is_public: bool | None = None
