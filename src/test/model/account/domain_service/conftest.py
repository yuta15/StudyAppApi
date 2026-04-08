import pytest

from src.app.model.account.entities.principals import AccountStatus
from src.app.model.account.service.change_account_status_domain_service import ChangeStatusData
from src.app.model.account.service.create_account_domain_service import CreateAccountResults
from src.app.model.account.service.delete_account_domain_service import DeleteAccountData
from src.app.model.account.service.update_subjects_domain_service import UpdateSubjectData


@pytest.fixture
def suspend_account(account):
    account.to_suspended()
    return account

@pytest.fixture
def deleted_account(account):
    account.to_delete()
    return account

@pytest.fixture
def updated_metadata(metadata):
    metadata.update()
    return metadata

@pytest.fixture
def deleted_metadata(metadata):
    metadata.delete()
    return metadata