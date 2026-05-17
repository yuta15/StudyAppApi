from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, OperationalError, TimeoutError

from src.app.model.account import AccountRepositoryInterface, Account
from src.app.schemas.db.account import AccountTable
from src.app.core.exceptions import DatabaseError, NetworkError, DataNotFoundError, InvalidDataError


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def save(self, account: Account) -> Account:
        try:
            account_table = self._get_account(principal_id=account.principal_id)
            if account_table:
                account_table.status = account.status
                return account
            else:
                add_account_table = AccountTable.from_account(account=account)
                self._session.add(add_account_table)
                return account
        except IntegrityError as e:
            raise InvalidDataError(f"Invalid data error {e}")
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")

    def get(self, principal_id: UUID) -> Account:
        try:
            account_table = self._get_account(principal_id=principal_id)
        except (OperationalError, TimeoutError) as e:
            raise NetworkError(f"Connection failed. {e}")
        except Exception as e:
            raise DatabaseError(f"Unknown error. {e}")
        if account_table is None:
            raise DataNotFoundError("Account not found.")
        return account_table.to_account()

    def _get_account(self, principal_id: UUID) -> AccountTable | None:
        stmt = select(AccountTable).where(AccountTable.principal_id == principal_id)
        account_table = self._session.exec(statement=stmt).one_or_none()
        return account_table
