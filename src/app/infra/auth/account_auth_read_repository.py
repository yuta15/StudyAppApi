from uuid import UUID

from sqlmodel import select, exists, Session

from src.app.service.interface.account import AccountAuthReadInterface
from src.app.model.account import AccountStatus
from src.app.schemas.db.account import AccountTable


class AccountAuthReadRepository(AccountAuthReadInterface):
    def __init__(self, session: Session):
        self._session = session

    def has_specified_active_user(self, principal_id: UUID) -> bool:
        stmt = select(
            exists().where(AccountTable.principal_id == principal_id, AccountTable.status == AccountStatus.ACTIVE)
        )
        return self._session.exec(stmt).one()
