from uuid import UUID

from sqlalchemy.exc import OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, NetworkError
from src.app.model.textbook import TitleString
from src.app.schemas.db.textbook import (
    ChapterTable,
    TextbookAuthorTable,
    TextbookChapterTable,
    TextbookMetadataTable,
    TextbookTable,
)
from src.app.service.interface.textbook import (
    MinimalReadChapter,
    MinimalReadTextbookMetadata,
    TextbookReadInterface,
    TextbookReadModel,
)


class TextbookReadRepository(TextbookReadInterface):
    def __init__(self, session: Session):
        self._session = session

    def fetch_textbook(self, textbook_id: UUID) -> TextbookReadModel:
        try:
            textbook_table, metadata_table = self._fetch_textbook_tables(textbook_id=textbook_id)
            author_ids = self._fetch_author_ids(textbook_id=textbook_id)
            chapters = self._fetch_chapters(textbook_id=textbook_id)
        except DataNotFoundError:
            raise
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}") from e
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}") from e

        return TextbookReadModel(
            textbook_id=textbook_table.textbook_id,
            title=TitleString(value=textbook_table.title),
            status=textbook_table.status,
            author_ids=author_ids,
            chapters=chapters,
            metadata=MinimalReadTextbookMetadata(
                created_at=metadata_table.created_at,
                updated_at=metadata_table.updated_at,
            ),
        )

    def _fetch_textbook_tables(self, textbook_id: UUID) -> tuple[TextbookTable, TextbookMetadataTable]:
        stmt = (
            select(TextbookTable, TextbookMetadataTable)
            .join(TextbookMetadataTable, TextbookMetadataTable.textbook_id == TextbookTable.textbook_id)
            .where(
                TextbookTable.textbook_id == textbook_id,
                TextbookMetadataTable.deleted_at.is_(None),
            )
        )
        result = self._session.exec(statement=stmt).one_or_none()
        if result is None:
            raise DataNotFoundError("Textbook not found.")
        return result

    def _fetch_author_ids(self, textbook_id: UUID) -> list[UUID]:
        stmt = (
            select(TextbookAuthorTable.principal_id)
            .where(TextbookAuthorTable.textbook_id == textbook_id)
            .order_by(TextbookAuthorTable.id)
        )
        return list(self._session.exec(statement=stmt).all())

    def _fetch_chapters(self, textbook_id: UUID) -> list[MinimalReadChapter]:
        stmt = (
            select(ChapterTable)
            .join(TextbookChapterTable, TextbookChapterTable.chapter_id == ChapterTable.chapter_id)
            .where(TextbookChapterTable.textbook_id == textbook_id)
            .order_by(TextbookChapterTable.position)
        )
        chapter_tables = self._session.exec(statement=stmt).all()
        read_chapters = []
        for chapter_table in chapter_tables:
            read_chapters.append(
                MinimalReadChapter(
                    chapter_id=chapter_table.chapter_id,
                    title=chapter_table.to_chapter().title,
                )
            )
        return read_chapters
