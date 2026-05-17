from uuid import UUID

from sqlalchemy.exc import OperationalError, TimeoutError
from sqlmodel import Session, exists, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, NetworkError
from src.app.schemas.db.textbook import (
    TextbookAuthorTable,
    TextbookMetadataTable,
    TextbookSettingsTable,
    TextbookTable,
)
from src.app.service.interface.textbook import TextbookAuthReadInterface, TextbookVisibility


class TextbookAuthReadRepository(TextbookAuthReadInterface):
    def __init__(self, session: Session):
        self._session = session

    def is_author(self, principal_id: UUID, textbook_id: UUID) -> bool:
        try:
            stmt = select(
                exists().where(
                    TextbookAuthorTable.principal_id == principal_id,
                    TextbookAuthorTable.textbook_id == textbook_id,
                    TextbookMetadataTable.textbook_id == textbook_id,
                    TextbookMetadataTable.deleted_at.is_(None),
                )
            )
            return self._session.exec(statement=stmt).one()
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}") from e
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}") from e

    def fetch_textbook_visibility(self, textbook_id: UUID) -> TextbookVisibility:
        try:
            stmt = (
                select(TextbookTable, TextbookSettingsTable)
                .join(TextbookSettingsTable, TextbookSettingsTable.textbook_id == TextbookTable.textbook_id)
                .join(TextbookMetadataTable, TextbookMetadataTable.textbook_id == TextbookTable.textbook_id)
                .where(
                    TextbookTable.textbook_id == textbook_id,
                    TextbookMetadataTable.deleted_at.is_(None),
                )
            )
            result = self._session.exec(statement=stmt).one_or_none()
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}") from e
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}") from e

        if result is None:
            raise DataNotFoundError("Textbook not found.")

        textbook_table, settings_table = result
        return TextbookVisibility(
            textbook_id=textbook_table.textbook_id,
            status=textbook_table.status,
            is_public=settings_table.is_public,
        )
