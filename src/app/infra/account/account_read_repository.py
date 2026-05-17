from uuid import UUID

from sqlalchemy.exc import OperationalError, TimeoutError
from sqlmodel import Session, select

from src.app.core.exceptions import DatabaseError, NetworkError
from src.app.model.account import AccountNameStrings
from src.app.schemas.db.account import AccountTable
from src.app.service.interface.account import AccountReadInterface, ReadMinimalAccount


class AccountReadRepository(AccountReadInterface):
    def __init__(self, session: Session):
        self._session = session

    def fetch_minimal_accounts(self, principal_ids: list[UUID]) -> list[ReadMinimalAccount]:
        try:
            stmt = select(AccountTable).where(AccountTable.principal_id.in_(principal_ids))
            account_tables = self._session.exec(statement=stmt).all()
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}") from e
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}") from e

        account_tables_by_id = {account_table.principal_id: account_table for account_table in account_tables}
        accounts: list[ReadMinimalAccount] = []
        for principal_id in principal_ids:
            account_table = account_tables_by_id.get(principal_id)
            if account_table is None:
                continue
            accounts.append(
                ReadMinimalAccount(
                    principal_id=principal_id, account_name=AccountNameStrings(value=account_table.account_name)
                )
            )
        return accounts
