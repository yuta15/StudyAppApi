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
class AuthorTextbookDTO:
    principal_id: UUID
    textbook_id: UUID
    author_id: UUID
