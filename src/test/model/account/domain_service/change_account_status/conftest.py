import pytest

from src.app.model.account.entities.principals import AccountStatus
from src.app.model.account.service.change_account_status_domain_service import ChangeStatusData


@pytest.fixture
def active_to_suspend(account, metadata):
    return ChangeStatusData(
        account=account,
        metadata=metadata,
        updated_status=AccountStatus.SUSPENDED
    )

@pytest.fixture
def active_to_deleted(account, metadata):
    return ChangeStatusData(
        account=account,
        metadata=metadata,
        updated_status=AccountStatus.DELETED
    )

@pytest.fixture
def suspend_to_active(suspend_account, updated_metadata):
    return ChangeStatusData(
        account=suspend_account,
        metadata=updated_metadata,
        updated_status=AccountStatus.ACTIVE
    )

@pytest.fixture
def suspend_to_delete(suspend_account, updated_metadata):
    return ChangeStatusData(
        account=suspend_account,
        metadata=updated_metadata,
        updated_status=AccountStatus.DELETED
    )

@pytest.fixture
def delete_to_active(deleted_account, deleted_metadata):
    return ChangeStatusData(
        account=deleted_account,
        metadata=deleted_metadata,
        updated_status=AccountStatus.ACTIVE
    )

@pytest.fixture
def delete_to_suspend(deleted_account, deleted_metadata):
    return ChangeStatusData(
        account=deleted_account,
        metadata=deleted_metadata,
        updated_status=AccountStatus.SUSPENDED
    )

@pytest.fixture
def invalid_value(account, metadata):
    return ChangeStatusData(
        account=account,
        metadata=metadata,
        updated_status="ACTIVE"
    )