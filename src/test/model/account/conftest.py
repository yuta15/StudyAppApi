import pytest

from src.test import const


@pytest.fixture
def password():
    return const.password

@pytest.fixture
def email():
    return const.email

@pytest.fixture
def display_name():
    return const.display_name

@pytest.fixture
def hashed_password():
    return const.hashed_password

@pytest.fixture
def account_id():
    return const.account_id