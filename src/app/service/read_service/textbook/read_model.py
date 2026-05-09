from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.app.model.textbook import TextbookStatus, TitleString
from src.app.service.read_service.account.read_model import ReadAccount


@dataclass
class ReadTextbookMetadata:
    created_at: datetime
    last_update: datetime
    deleted_at: datetime | None = None


@dataclass
class ReadTextbookSettings:
    is_public: bool


@dataclass
class ReadChapter:
    chapter_id: UUID
    title: TitleString | None
    content: str


@dataclass
class ReadTextbook:
    textbook_id: UUID
    title: TitleString
    status: TextbookStatus
    authors: list[ReadAccount]
    metadata: ReadTextbookMetadata
    settings: ReadTextbookSettings
    chapters: list[ReadChapter]
