import pytest


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