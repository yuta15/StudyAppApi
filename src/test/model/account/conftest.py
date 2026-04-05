import pytest

from src.test import const

@pytest.fixture
def account_name():
    return const.account_name

@pytest.fixture
def name():
    return const.name

@pytest.fixture
def email():
    return const.email

@pytest.fixture
def hashed_password():
    return const.hashed_password