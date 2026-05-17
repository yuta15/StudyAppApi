from uuid import UUID

from sqlalchemy.exc import OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, NetworkError
from src.app.model.account import AllowedIdentityProvider
from src.app.schemas.db.account import AccountIdentityTable
from src.app.service.interface.account import AccountIdentityReadInterface


class AccountIdentityReadRepository(AccountIdentityReadInterface):
    def __init__(self, session: Session):
        self._session = session

    def resolve_principal_id(self, subject: str, provider: AllowedIdentityProvider) -> UUID | None:
        try:
            stmt = select(AccountIdentityTable.principal_id).where(
                AccountIdentityTable.subject == subject,
                AccountIdentityTable.provider == provider,
            )
            return self._session.exec(statement=stmt).one_or_none()
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}") from e
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}") from e
