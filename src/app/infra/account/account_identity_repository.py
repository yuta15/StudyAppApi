from uuid import UUID

from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, DataNotFoundError, InvalidDataError, NetworkError
from src.app.model.account import AccountIdentityRepositoryInterface, AccountIdentity
from src.app.schemas.db.account import AccountIdentityTable


class AccountIdentityRepository(AccountIdentityRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, identity: AccountIdentity) -> AccountIdentity:
        try:
            identity_table = self._get_identity(principal_id=identity.principal_id)
            if identity_table:
                identity_table.subject = identity.subject
                identity_table.provider = identity.provider
                return identity
            else:
                identity_table = AccountIdentityTable.from_identity(identity=identity)
                self._session.add(identity_table)
                return identity
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, principal_id: UUID) -> AccountIdentity:
        try:
            identity_table = self._get_identity(principal_id=principal_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")
        if identity_table is None:
            raise DataNotFoundError("Account identity not found.")
        return identity_table.to_identity()

    def delete(self, principal_id: UUID) -> None:
        try:
            identity_table = self._get_identity(principal_id=principal_id)
            if identity_table is None:
                raise DataNotFoundError("Identity not found error")
            self._session.delete(identity_table)
        except DataNotFoundError:
            raise
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def _get_identity(self, principal_id: UUID) -> AccountIdentityTable | None:
        stmt = select(AccountIdentityTable).where(AccountIdentityTable.principal_id == principal_id)
        return self._session.exec(statement=stmt).one_or_none()
