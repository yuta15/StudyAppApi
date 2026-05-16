from datetime import datetime
from uuid import UUID

from sqlalchemy import UniqueConstraint, Text, DateTime
from sqlmodel import Field

from src.app.schemas.db.base import TableBase
from src.app.model.textbook import TextbookStatus


class TextbookTable(TableBase, table=True):
    __tablename__ = "textbook"

    textbook_id: UUID = Field(unique=True)
    title: str = Field(max_length=128)
    status: TextbookStatus


class TextbookAuthorTable(TableBase, table=True):
    __tablename__ = "textbook_author"
    __table_args__ = (UniqueConstraint("textbook_id", "principal_id", name="uq_textbook_author"),)

    textbook_id: UUID
    principal_id: UUID = Field(index=True)


class TextbookChapterTable(TableBase, table=True):
    __tablename__ = "textbook_chapter"
    __table_args__ = (UniqueConstraint("textbook_id", "chapter_id", name="uq_textbook_chapter"),)

    textbook_id: UUID = Field(index=True)
    chapter_id: UUID
    position: int


class TextbookMetadataTable(TableBase, table=True):
    __tablename__ = "textbook_metadata"

    textbook_id: UUID = Field(unique=True)
    created_at: datetime = Field(sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(sa_type=DateTime(timezone=True))
    deleted_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))


class TextbookSettingsTable(TableBase, table=True):
    __tablename__ = "textbook_settings"

    textbook_id: UUID = Field(unique=True)
    is_public: bool


class ChapterTable(TableBase, table=True):
    __tablename__ = "chapter"

    chapter_id: UUID = Field(unique=True)
    title: str = Field(max_length=128)
    content: str = Field(sa_type=Text)
