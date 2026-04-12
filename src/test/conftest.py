from uuid import UUID

import pytest

from src.test import const
from src.app.model.account.entities.subjects import AllowedIdentityProvider


@pytest.fixture
def account_principal_id():
    return UUID(const.account_principal_id)

@pytest.fixture
def identity_provider():
    return AllowedIdentityProvider.FIREBASE

@pytest.fixture
def identity_subject():
    return const.identity_subject