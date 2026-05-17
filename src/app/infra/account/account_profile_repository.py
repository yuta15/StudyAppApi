from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError

from src.app.model.account import AccountProfileRepositoryInterface, AccountProfile
from src.app.schemas.db.account import AccountProfileTable
from src.app.core.exceptions import DatabaseError, NetworkError, DataNotFoundError, InvalidDataError


class AccountProfileRepository(AccountProfileRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, profile: AccountProfile) -> AccountProfile:
        try:
            profile_table = self._get_profile(principal_id=profile.principal_id)
            if profile_table:
                profile_table.display_name = profile.display_name
                profile_table.email = profile.email.value
                profile_table.country = profile.country
            else:
                self._session.add(AccountProfileTable.from_profile(profile=profile))
            return profile
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, principal_id: UUID) -> AccountProfile:
        try:
            profile_table = self._get_profile(principal_id=principal_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

        if profile_table is None:
            raise DataNotFoundError("Account profile not found.")
        return profile_table.to_profile()

    def _get_profile(self, principal_id: UUID) -> AccountProfileTable | None:
        stmt = select(AccountProfileTable).where(AccountProfileTable.principal_id == principal_id)
        return self._session.exec(statement=stmt).one_or_none()
