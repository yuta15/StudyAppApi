from uuid import UUID

import pytest

from src.test import const
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.value_object import AccountNameStrings, EmailStrings
from src.app.model.account.entities.subjects import (
    AccountProfile,
    AccountBasicSettings,
    AccountAuthSettings
)


@pytest.fixture
def account_principal_id():
    return UUID(const.account_principal_id)

@pytest.fixture
def account_name():
    return AccountNameStrings(const.account_name)

@pytest.fixture
def display_name():
    return const.display_name

@pytest.fixture
def email():
    return EmailStrings(const.email)

@pytest.fixture
def hashed_password():
    return const.hashed_password

@pytest.fixture
def account(account_name):
    return Account.new(account_name=account_name)

@pytest.fixture
def profile(account_principal_id, display_name, email):
    return AccountProfile.new(principal_id=account_principal_id, display_name=display_name, email=email)

@pytest.fixture
def basic_settings(account_principal_id):
    return AccountBasicSettings.new(principal_id=account_principal_id)

@pytest.fixture
def auth_settings(account_principal_id, hashed_password):
    return AccountAuthSettings.new(principal_id=account_principal_id, hashed_password=hashed_password)

@pytest.fixture
def metadata(account_principal_id):
    return AccountMetadata.new(account_principal_id)