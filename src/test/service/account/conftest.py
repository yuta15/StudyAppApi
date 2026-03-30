import pytest

from src.test import const
from src.app.schemas.api.account.account_schema import CreateAccountInput
from src.test.service.account.account_repository_for_test import PasswordHasherForTest, AccountRepositorySuccess


@pytest.fixture
def create_account_input():
    return CreateAccountInput(
        display_name=const.display_name,
        email=const.email,
        password=const.password
    )

@pytest.fixture
def hashed_password():
    return const.hashed_password

@pytest.fixture
def password_hasher_success():
    return PasswordHasherForTest()

@pytest.fixture
def account_repository_success():
    return AccountRepositorySuccess()

