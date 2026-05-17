import pytest


@pytest.fixture
def suspend_account(account_generator):
    account = account_generator()
    account.to_suspended()
    return account


@pytest.fixture
def deleted_account(account_generator):
    account = account_generator()
    account.to_delete()
    return account


@pytest.fixture
def updated_metadata(metadata_generator):
    metadata = metadata_generator()
    metadata.update()
    return metadata


@pytest.fixture
def deleted_metadata(metadata_generator):
    metadata = metadata_generator()
    metadata.delete()
    return metadata
