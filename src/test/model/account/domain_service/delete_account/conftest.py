import pytest

from src.app.model.account.service.delete_account_domain_service import DeleteAccountData


@pytest.fixture
def active_account_data(account, metadata, profile, basic_settings):
    return DeleteAccountData(
        account=account,
        metadata=metadata,
        profile=profile,
        basic_settings=basic_settings
    )

@pytest.fixture
def suspended_account_data(suspend_account, updated_metadata, profile, basic_settings):
     return DeleteAccountData(
        account=suspend_account,
        metadata=updated_metadata,
        profile=profile,
        basic_settings=basic_settings
    )

@pytest.fixture
def deleted_account_data(deleted_account, deleted_metadata, profile, basic_settings):
     return DeleteAccountData(
        account=deleted_account,
        metadata=deleted_metadata,
        profile=profile,
        basic_settings=basic_settings
    )