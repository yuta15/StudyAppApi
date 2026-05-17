from datetime import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import UniqueConstraint, Text, DateTime
from sqlmodel import Field

from src.app.schemas.db.base import TableBase
from src.app.model.textbook import Chapter, Textbook, TextbookMetadata, TextbookSettings, TextbookStatus, TitleString


class TextbookTable(TableBase, table=True):
    __tablename__ = "textbook"

    textbook_id: UUID = Field(unique=True)
    title: str = Field(max_length=128)
    status: TextbookStatus

    @classmethod
    def from_textbook(cls, textbook: Textbook) -> Self:
        return cls(
            textbook_id=textbook.textbook_id,
            title=textbook.title.value,
            status=textbook.status,
        )

    def to_textbook(self, author_ids: list[UUID], chapter_ids: list[UUID]) -> Textbook:
        return Textbook(
            textbook_id=self.textbook_id,
            title=TitleString(value=self.title),
            author_ids=author_ids,
            chapter_ids=chapter_ids,
            status=self.status,
        )


class ChapterTable(TableBase, table=True):
    __tablename__ = "chapter"

    chapter_id: UUID = Field(unique=True)
    title: str = Field(max_length=128)
    content: str = Field(sa_type=Text)

    @classmethod
    def from_chapter(cls, chapter: Chapter) -> Self:
        return cls(
            chapter_id=chapter.chapter_id,
            title=chapter.title.value,
            content=chapter.content,
        )

    def to_chapter(self) -> Chapter:
        return Chapter(
            chapter_id=self.chapter_id,
            title=TitleString(value=self.title),
            content=self.content,
        )


class TextbookAuthorTable(TableBase, table=True):
    __tablename__ = "textbook_author"
    __table_args__ = (UniqueConstraint("textbook_id", "principal_id", name="uq_textbook_author"),)

    textbook_id: UUID = Field(foreign_key="textbook.textbook_id")
    principal_id: UUID = Field(index=True, foreign_key="account.principal_id")


class TextbookChapterTable(TableBase, table=True):
    __tablename__ = "textbook_chapter"
    __table_args__ = (UniqueConstraint("textbook_id", "chapter_id", name="uq_textbook_chapter"),)

    textbook_id: UUID = Field(index=True, foreign_key="textbook.textbook_id")
    chapter_id: UUID = Field(foreign_key="chapter.chapter_id")
    position: int


class TextbookMetadataTable(TableBase, table=True):
    __tablename__ = "textbook_metadata"

    textbook_id: UUID = Field(unique=True, foreign_key="textbook.textbook_id")
    created_at: datetime = Field(sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(sa_type=DateTime(timezone=True))
    deleted_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))

    @classmethod
    def from_metadata(cls, metadata: TextbookMetadata) -> Self:
        return cls(
            textbook_id=metadata.textbook_id,
            created_at=metadata.created_at,
            updated_at=metadata.updated_at,
            deleted_at=metadata.deleted_at,
        )

    def to_metadata(self) -> TextbookMetadata:
        return TextbookMetadata(
            textbook_id=self.textbook_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )


class TextbookSettingsTable(TableBase, table=True):
    __tablename__ = "textbook_settings"

    textbook_id: UUID = Field(unique=True, foreign_key="textbook.textbook_id")
    is_public: bool

    @classmethod
    def from_settings(cls, textbook_settings: TextbookSettings) -> Self:
        return cls(
            textbook_id=textbook_settings.textbook_id,
            is_public=textbook_settings.is_public,
        )

    def to_settings(self) -> TextbookSettings:
        return TextbookSettings(
            textbook_id=self.textbook_id,
            is_public=self.is_public,
        )
