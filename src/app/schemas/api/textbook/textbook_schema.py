from datetime import datetime
from uuid import UUID

from src.app.model.textbook import TextbookStatus
from src.app.schemas.api.base import ApiModel


class CreateTextbookInput(ApiModel):
    title: str


class CreateTextbookOutput(ApiModel):
    textbook_id: UUID


class ModifyTextbookInput(ApiModel):
    title: str | None = None
    status: TextbookStatus | None = None


class TextbookMetadataOutput(ApiModel):
    created_at: datetime
    updated_at: datetime


class ModifyTextbookOutput(ApiModel):
    textbook_id: UUID
    title: str
    status: TextbookStatus
    metadata: TextbookMetadataOutput


class AddAuthorInput(ApiModel):
    author_id: UUID


class AddChapterInput(ApiModel):
    chapter_title: str


class AddChapterOutput(ApiModel):
    chapter_id: UUID


class ReorderChaptersInput(ApiModel):
    chapter_ids: list[UUID]


class ModifyChapterInput(ApiModel):
    title: str | None = None
    content: str | None = None


class ChapterOutput(ApiModel):
    chapter_id: UUID
    title: str | None
    content: str


class ModifyTextbookSettingsInput(ApiModel):
    is_public: bool | None = None


class TextbookSettingsValueOutput(ApiModel):
    is_public: bool


class TextbookSettingsOutput(ApiModel):
    textbook_id: UUID
    settings: TextbookSettingsValueOutput


class MinimalAccountOutput(ApiModel):
    principal_id: UUID
    account_name: str


class MinimalChapterOutput(ApiModel):
    chapter_id: UUID
    title: str


class TextbookOutput(ApiModel):
    textbook_id: UUID
    title: str
    status: TextbookStatus
    authors: list[MinimalAccountOutput]
    chapters: list[MinimalChapterOutput]
    metadata: TextbookMetadataOutput
