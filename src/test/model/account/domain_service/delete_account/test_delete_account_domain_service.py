from datetime import datetime

import pytest

from src.app.model.account import AccountStatus, DeleteAccountDomainService, EmailStrings


def test_from_active_success(active_account_data):
    DeleteAccountDomainService.exec(active_account_data)
    MASK_VALUE = "XXXXXXXXXX"
    assert active_account_data.account.status == AccountStatus.DELETED
    assert isinstance(active_account_data.metadata.deleted_at, datetime)
    assert active_account_data.profile.email == EmailStrings(f"{MASK_VALUE}@{MASK_VALUE}")
    assert active_account_data.profile.display_name == MASK_VALUE
    assert not active_account_data.basic_settings.is_public
    assert active_account_data.identity.subject == MASK_VALUE


def test_from_suspended_success(suspended_account_data):
    DeleteAccountDomainService.exec(suspended_account_data)
    MASK_VALUE = "XXXXXXXXXX"
    assert suspended_account_data.account.status == AccountStatus.DELETED
    assert isinstance(suspended_account_data.metadata.deleted_at, datetime)
    assert suspended_account_data.profile.email == EmailStrings(f"{MASK_VALUE}@{MASK_VALUE}")
    assert suspended_account_data.profile.display_name == MASK_VALUE
    assert not suspended_account_data.basic_settings.is_public
    assert suspended_account_data.identity.subject == MASK_VALUE


def test_from_deleted_failure(deleted_account_data):
    with pytest.raises(Exception):
        DeleteAccountDomainService.exec(deleted_account_data)
