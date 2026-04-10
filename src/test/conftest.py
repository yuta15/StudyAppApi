from uuid import UUID

import pytest

from src.test import const


@pytest.fixture
def account_principal_id():
    return UUID(const.account_principal_id)

@pytest.fixture
def account_subject_id():
    return UUID(const.subject_id)