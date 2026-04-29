from uuid import UUID

import pytest

from src.app.model.account.entities.subjects import AllowedIdentityProvider
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.value_object import AccountNameStrings, EmailStrings
from src.app.model.account.entities.subjects import (
    AccountProfile,
    AccountBasicSettings,
    AccountIdentity,
)
from src.test import const
from src.test.dummy_session import DummySession


@pytest.fixture
def dummy_session():
    return DummySession()


@pytest.fixture
def account_principal_id():
    return UUID(const.account_principal_id)


@pytest.fixture
def metadata_id():
    return UUID(const.metadata_id)


@pytest.fixture
def identity_provider():
    return AllowedIdentityProvider.FIREBASE


@pytest.fixture
def identity_subject():
    return const.identity_subject


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
def account_generator(account_name, account_principal_id):
    def generator():
        account = Account.new(account_name=account_name)
        account.principal_id = account_principal_id
        return account

    return generator


@pytest.fixture
def profile_generator(account_principal_id, display_name, email):
    def generator():
        return AccountProfile.new(principal_id=account_principal_id, display_name=display_name, email=email)

    return generator


@pytest.fixture
def basic_settings_generator(account_principal_id):
    def generator():
        return AccountBasicSettings.new(principal_id=account_principal_id)

    return generator


@pytest.fixture
def metadata_generator(account_principal_id, metadata_id):
    def generator():
        metadata = AccountMetadata.new(account_principal_id)
        metadata.metadata_id = metadata_id
        return metadata

    return generator


@pytest.fixture
def identity_generator(account_principal_id, identity_provider, identity_subject):
    def generator():
        return AccountIdentity.new(
            principal_id=account_principal_id,
            provider=identity_provider,
            subject=identity_subject,
        )

    return generator
