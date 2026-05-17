import pytest
from sqlmodel import select

from src.app.core.exceptions import DataNotFoundError
from src.app.infra.account import AccountRepository
from src.app.model.account import Account, AccountStatus
from src.app.schemas.db.account import AccountTable

pytestmark = pytest.mark.integration


def test_save_success_creates_account(
    infra_session,
    account_principal_id,
    account_name,
):
    """Account保存時にDBへ新規追加できること。"""
    # Arrange
    repository = AccountRepository(session=infra_session)
    account = Account(
        principal_id=account_principal_id,
        account_name=account_name,
        status=AccountStatus.ACTIVE,
    )

    # Act
    repository.save(account=account)
    infra_session.flush()

    # Assert
    account_table = infra_session.exec(
        select(AccountTable).where(AccountTable.principal_id == account_principal_id)
    ).one()
    assert account_table.account_name == account_name.value
    assert account_table.status == AccountStatus.ACTIVE


def test_save_success_updates_account_status(
    infra_session,
    persisted_account_table,
    account_principal_id,
    account_name,
):
    """既存Account保存時にstatusだけを更新できること。"""
    # Arrange
    repository = AccountRepository(session=infra_session)
    account = Account(
        principal_id=account_principal_id,
        account_name=account_name,
        status=AccountStatus.SUSPENDED,
    )

    # Act
    repository.save(account=account)
    infra_session.flush()

    # Assert
    assert persisted_account_table.account_name == account_name.value
    assert persisted_account_table.status == AccountStatus.SUSPENDED


def test_get_success_returns_account(
    infra_session,
    persisted_account_table,
    account_principal_id,
    account_name,
):
    """DB値からAccountNameStringsを持つAccountを復元できること。"""
    # Arrange
    repository = AccountRepository(session=infra_session)

    # Act
    account = repository.get(principal_id=account_principal_id)

    # Assert
    assert account == Account(
        principal_id=account_principal_id,
        account_name=account_name,
        status=persisted_account_table.status,
    )


def test_get_failure_missing_account(
    infra_session,
    account_principal_id,
):
    """存在しないAccountの取得ではDataNotFoundErrorになること。"""
    # Arrange
    repository = AccountRepository(session=infra_session)

    # Assert
    with pytest.raises(DataNotFoundError):
        repository.get(principal_id=account_principal_id)
