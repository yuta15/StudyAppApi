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
    principal_id: UUID
    textbook_id: UUID


@dataclass
class ModifyTextbookDTO:
    principal_id: UUID
    textbook_id: UUID
    title: TitleString | None = None
    status: TextbookStatus | None = None


@dataclass
class ModifyTextbookSettingsDTO:
    principal_id: UUID
    textbook_id: UUID
    is_public: bool | None = None


@dataclass
class AddChapterDTO:
    principal_id: UUID
    textbook_id: UUID
    title: TitleString


@dataclass
class ModifyChapterDTO:
    principal_id: UUID
    textbook_id: UUID
    chapter_id: UUID
    title: TitleString | None = None
    content: str | None = None


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
class AddAuthorDTO:
    principal_id: UUID
    textbook_id: UUID
    author_id: UUID


@dataclass
class RemoveAuthorDTO:
    principal_id: UUID
    textbook_id: UUID
    author_id: UUID


@dataclass
class OutputTextbookMetadata:
    created_at: datetime
    last_update: datetime


@dataclass
class OutputTextbookSettings:
    is_public: bool


@dataclass
class OutputChapter:
    chapter_id: UUID
    title: TitleString | None
    content: str


@dataclass
class OutputTextbookDetails:
    textbook_id: UUID
    title: TitleString
    status: TextbookStatus
    author_ids: list[UUID]
    metadata: OutputTextbookMetadata
    settings: OutputTextbookSettings
    chapters: list[OutputChapter]


@dataclass
class OutputTextbookMinimal:
    metadata: OutputTextbookMetadata
    textbook_id: UUID
    title: TitleString
