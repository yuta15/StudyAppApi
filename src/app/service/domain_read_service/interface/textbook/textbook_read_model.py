from datetime import datetime
from uuid import UUID
from dataclasses import dataclass

from src.app.model.textbook.entities.value_object import TextbookStatus, TitleString


@dataclass
class MinimalReadChapter:
    chapter_id: UUID
    title: TitleString


@dataclass
class MinimalReadTextbookMetadata:
    created_at: datetime
    updated_at: datetime


@dataclass
class MinimalReadTextbookSettings:
    is_public: bool


@dataclass
class TextbookReadModel:
    textbook_id: UUID
    title: TitleString
    status: TextbookStatus
    author_ids: list[UUID]
    chapters: list[MinimalReadChapter]
    metadata: MinimalReadTextbookMetadata


@dataclass
class TextbookVisibility:
    textbook_id: UUID
    status: TextbookStatus
    is_public: bool
