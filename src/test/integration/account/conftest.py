import pytest

from src.app.model.account import AccountStatus
from src.app.schemas.db.account import AccountTable


@pytest.fixture
def persisted_account_table(infra_session, account_principal_id, account_name):
    account_table = AccountTable(
        principal_id=account_principal_id,
        account_name=account_name.value,
        status=AccountStatus.ACTIVE,
    )
    infra_session.add(account_table)
    infra_session.flush()
    return account_table
