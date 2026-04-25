import pytest

from src.test.service.dummy_account_auth_repository import DummyAccuntAuthReader
from src.app.service.authorization_service.models import AccountAuthInput
from src.app.model.account.entities.subjects import AccountSubjects


@pytest.fixture
def found_account_auth_reader():
    return DummyAccuntAuthReader(result=True)

@pytest.fixture
def not_found_account_auth_reader():
    return DummyAccuntAuthReader(result=False)

@pytest.fixture
def negative_account_auth_reader():
    return DummyAccuntAuthReader(result=True, is_negative=True)