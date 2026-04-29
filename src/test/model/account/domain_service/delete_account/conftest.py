import pytest

from src.app.model.account.service.delete_account_domain_service import (
    DeleteAccountData,
)


@pytest.fixture
def active_account_data(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return DeleteAccountData(
        account=account_generator(),
        metadata=metadata_generator(),
        profile=profile_generator(),
        basic_settings=basic_settings_generator(),
        identity=identity_generator(),
    )


@pytest.fixture
def suspended_account_data(
    suspend_account,
    updated_metadata,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return DeleteAccountData(
        account=suspend_account,
        metadata=updated_metadata,
        profile=profile_generator(),
        basic_settings=basic_settings_generator(),
        identity=identity_generator(),
    )


@pytest.fixture
def deleted_account_data(
    deleted_account,
    deleted_metadata,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return DeleteAccountData(
        account=deleted_account,
        metadata=deleted_metadata,
        profile=profile_generator(),
        basic_settings=basic_settings_generator(),
        identity=identity_generator(),
    )
