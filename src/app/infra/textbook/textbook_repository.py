from uuid import UUID

from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, InvalidDataError, NetworkError
from src.app.model.textbook import Textbook, TextbookRepositoryInterface
from src.app.schemas.db.textbook import TextbookAuthorTable, TextbookChapterTable, TextbookTable


class TextbookRepository(TextbookRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, textbook: Textbook) -> Textbook:
        try:
            textbook_table = self._get_textbook(textbook_id=textbook.textbook_id)
            if textbook_table:
                textbook_table.title = textbook.title.value
                textbook_table.status = textbook.status
            else:
                self._session.add(TextbookTable.from_textbook(textbook=textbook))

            self._sync_authors(textbook=textbook)
            self._sync_chapters(textbook=textbook)
            return textbook
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, textbook_id: UUID) -> Textbook:
        try:
            textbook_table = self._get_textbook(textbook_id=textbook_id)
            if textbook_table is None:
                raise DataNotFoundError("Textbook not found.")
            author_tables = self._get_author_tables(textbook_id=textbook_id)
            chapter_tables = self._get_chapter_tables(textbook_id=textbook_id)

            author_ids = [author_table.principal_id for author_table in author_tables]
            chapter_ids = [chapter_table.chapter_id for chapter_table in chapter_tables]

        except DataNotFoundError:
            raise
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

        return textbook_table.to_textbook(author_ids=author_ids, chapter_ids=chapter_ids)

    def _get_textbook(self, textbook_id: UUID) -> TextbookTable | None:
        stmt = select(TextbookTable).where(TextbookTable.textbook_id == textbook_id)
        return self._session.exec(statement=stmt).one_or_none()

    def _get_author_tables(self, textbook_id: UUID) -> list[TextbookAuthorTable]:
        stmt = (
            select(TextbookAuthorTable)
            .where(TextbookAuthorTable.textbook_id == textbook_id)
            .order_by(TextbookAuthorTable.id)
        )
        return list(self._session.exec(statement=stmt).all())

    def _get_chapter_tables(self, textbook_id: UUID) -> list[TextbookChapterTable]:
        stmt = (
            select(TextbookChapterTable)
            .where(TextbookChapterTable.textbook_id == textbook_id)
            .order_by(TextbookChapterTable.position)
        )
        return list(self._session.exec(statement=stmt).all())

    def _sync_authors(self, textbook: Textbook) -> None:
        author_tables = self._get_author_tables(textbook_id=textbook.textbook_id)
        author_tables_by_id = {author_table.principal_id: author_table for author_table in author_tables}

        # 含まれていないauthorを削除
        for author_table in author_tables:
            if author_table.principal_id not in textbook.author_ids:
                self._session.delete(author_table)

        # DBに存在しないauthorを追加
        for author_id in textbook.author_ids:
            if author_id not in author_tables_by_id:
                self._session.add(
                    TextbookAuthorTable(
                        textbook_id=textbook.textbook_id,
                        principal_id=author_id,
                    )
                )

    def _sync_chapters(self, textbook: Textbook) -> None:
        chapter_tables = self._get_chapter_tables(textbook_id=textbook.textbook_id)
        chapter_tables_by_id = {chapter_table.chapter_id: chapter_table for chapter_table in chapter_tables}

        for chapter_table in chapter_tables:
            if chapter_table.chapter_id not in textbook.chapter_ids:
                self._session.delete(chapter_table)

        for position, chapter_id in enumerate(textbook.chapter_ids):
            chapter_table = chapter_tables_by_id.get(chapter_id)
            if chapter_table:
                chapter_table.position = position
            else:
                self._session.add(
                    TextbookChapterTable(
                        textbook_id=textbook.textbook_id,
                        chapter_id=chapter_id,
                        position=position,
                    )
                )
