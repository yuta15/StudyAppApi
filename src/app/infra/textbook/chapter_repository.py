from uuid import UUID

from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, InvalidDataError, NetworkError
from src.app.model.textbook import Chapter, ChapterRepositoryInterface
from src.app.schemas.db.textbook import ChapterTable


class ChapterRepository(ChapterRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, chapter: Chapter) -> Chapter:
        try:
            chapter_table = self._get_chapter(chapter_id=chapter.chapter_id)
            if chapter_table:
                chapter_table.title = chapter.title.value
                chapter_table.content = chapter.content
            else:
                self._session.add(ChapterTable.from_chapter(chapter=chapter))
            return chapter
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, chapter_id: UUID) -> Chapter:
        try:
            chapter_table = self._get_chapter(chapter_id=chapter_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

        if chapter_table is None:
            raise DataNotFoundError("Chapter not found.")
        return chapter_table.to_chapter()

    def _get_chapter(self, chapter_id: UUID) -> ChapterTable | None:
        stmt = select(ChapterTable).where(ChapterTable.chapter_id == chapter_id)
        return self._session.exec(statement=stmt).one_or_none()
