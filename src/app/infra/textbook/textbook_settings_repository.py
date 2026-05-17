from uuid import UUID

from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, InvalidDataError, NetworkError
from src.app.model.textbook import TextbookSettings, TextbookSettingsRepositoryInterface
from src.app.schemas.db.textbook import TextbookSettingsTable


class TextbookSettingsRepository(TextbookSettingsRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, textbook_settings: TextbookSettings) -> TextbookSettings:
        try:
            settings_table = self._get_settings(textbook_id=textbook_settings.textbook_id)
            if settings_table:
                settings_table.is_public = textbook_settings.is_public
            else:
                self._session.add(TextbookSettingsTable.from_settings(textbook_settings=textbook_settings))
            return textbook_settings
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, textbook_id: UUID) -> TextbookSettings:
        try:
            settings_table = self._get_settings(textbook_id=textbook_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

        if settings_table is None:
            raise DataNotFoundError("Textbook settings not found.")
        return settings_table.to_settings()

    def _get_settings(self, textbook_id: UUID) -> TextbookSettingsTable | None:
        stmt = select(TextbookSettingsTable).where(TextbookSettingsTable.textbook_id == textbook_id)
        return self._session.exec(statement=stmt).one_or_none()
