import pytest

from src.test.service.dummy_account_auth_repository import DummyAccuntAuthReader
from src.app.service.authorization_service.models import AccountAuthInput
from src.app.model.account.entities.subjects import AccountSubjects


@pytest.fixture
def success_account_repo():
    return DummyAccuntAuthReader(result=True)

@pytest.fixture
def failed_account_repo():
    return DummyAccuntAuthReader(result=False)

@pytest.fixture
def profile_account_auth_input(account_principal_id, account_subject_id):
    return AccountAuthInput(
        principal_id=account_principal_id,
        subject_id=account_subject_id,
        subject_type=AccountSubjects.ACCOUNT_PROFILE
    )

@pytest.fixture
def basic_settings_account_auth_input(account_principal_id, account_subject_id):
    return AccountAuthInput(
        principal_id=account_principal_id,
        subject_id=account_subject_id,
        subject_type=AccountSubjects.ACCOUNT_BASIC_SETTINGS
    )

@pytest.fixture
def auth_settings_account_auth_input(account_principal_id, account_subject_id):
    return AccountAuthInput(
        principal_id=account_principal_id,
        subject_id=account_subject_id,
        subject_type=AccountSubjects.ACCOUNT_AUTH_SETTINGS
    )