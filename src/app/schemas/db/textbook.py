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


class ChapterTable(TableBase, table=True):
    __tablename__ = "chapter"

    chapter_id: UUID = Field(unique=True)
    title: str = Field(max_length=128)
    content: str = Field(sa_type=Text)


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


class TextbookSettingsTable(TableBase, table=True):
    __tablename__ = "textbook_settings"

    textbook_id: UUID = Field(unique=True, foreign_key="textbook.textbook_id")
    is_public: bool
