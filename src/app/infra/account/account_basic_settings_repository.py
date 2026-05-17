from uuid import UUID

from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, InvalidDataError, NetworkError
from src.app.model.account import AccountBasicSettings, AccountBasicSettingsRepositoryInterface
from src.app.schemas.db.account import AccountBasicSettingsTable


class AccountBasicSettingsRepository(AccountBasicSettingsRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, basic_settings: AccountBasicSettings) -> AccountBasicSettings:
        try:
            basic_settings_table = self._get_basic_settings(principal_id=basic_settings.principal_id)
            if basic_settings_table:
                basic_settings_table.is_public = basic_settings.is_public
            else:
                self._session.add(AccountBasicSettingsTable.from_basic_settings(basic_settings=basic_settings))
            return basic_settings
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, principal_id: UUID) -> AccountBasicSettings:
        try:
            basic_settings_table = self._get_basic_settings(principal_id=principal_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

        if basic_settings_table is None:
            raise DataNotFoundError("Account basic settings not found.")
        return basic_settings_table.to_basic_settings()

    def _get_basic_settings(self, principal_id: UUID) -> AccountBasicSettingsTable | None:
        stmt = select(AccountBasicSettingsTable).where(AccountBasicSettingsTable.principal_id == principal_id)
        return self._session.exec(statement=stmt).one_or_none()
