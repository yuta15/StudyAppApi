from uuid import UUID

import pytest

from src.test import const
from src.test.service.dummy_account_auth_repository import DummyAccuntAuthReader


@pytest.fixture
def found_account_auth_reader():
    return DummyAccuntAuthReader(result=True)


@pytest.fixture
def not_found_account_auth_reader():
    return DummyAccuntAuthReader(result=False)


@pytest.fixture
def negative_account_auth_reader():
    return DummyAccuntAuthReader(result=True, is_negative=True)


@pytest.fixture
def textbook_id():
    return UUID(const.textbook_id)
