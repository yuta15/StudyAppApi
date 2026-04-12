import pytest

from src.app.model.account.entities.value_object import EmailStrings
from src.app.model.account.entities.subjects import (
    Country,
    AllowedIdentityProvider,
    AccountProfile,
    AccountBasicSettings,
    AccountIdentity
)


def test_profile_new(account_principal_id, display_name, email):
    profile = AccountProfile.new(principal_id=account_principal_id, display_name=display_name, email=email)
    assert profile.principal_id == account_principal_id
    assert profile.display_name == display_name
    assert profile.email == email
    assert profile.country == Country.NOT_SET

def test_profile_set_display_name_success(profile):
    new_display_name = "new_display_name"
    profile.set_display_name(display_name=new_display_name)
    assert profile.display_name == new_display_name

def test_profile_set_display_name_failure(profile):
    new_display_name = 1
    with pytest.raises(Exception):
        profile.set_display_name(display_name=new_display_name)

def test_profile_set_email_success(profile):
    email = EmailStrings("new_email@example.com")
    profile.set_email(email=email)
    assert profile.email == email

def test_profile_set_email_failure(profile):
    email = 1
    with pytest.raises(Exception):
        profile.set_email(email=email)

def test_profile_set_country_success(profile):
    profile.set_country(Country.JP)
    assert profile.country == Country.JP

def test_profile_set_country_failure(profile):
    country = "JP"
    with pytest.raises(Exception):
        profile.set_country(country=country)

def test_profile_delete(profile):
    profile.delete()
    MASK_VALUE = "XXXXXXXXXX"
    assert profile.display_name == MASK_VALUE
    assert profile.email == EmailStrings(f"{MASK_VALUE}@{MASK_VALUE}")


def test_basic_settings_new(account_principal_id):
    basic_settings = AccountBasicSettings.new(principal_id=account_principal_id)
    assert basic_settings.principal_id == account_principal_id
    assert basic_settings.is_public == True

def test_basic_settings_is_public_success(basic_settings):
    basic_settings.set_is_public(is_public=False)
    assert basic_settings.is_public == False

def test_basic_settings_is_public_failure(basic_settings):
    with pytest.raises(Exception):
        basic_settings.set_is_public(is_public=1)

def test_basic_settings_delete(basic_settings):
    basic_settings.delete()
    assert basic_settings.is_public == False


@pytest.mark.parametrize(
        ["provider", "subject"],
        [
            [AllowedIdentityProvider.FIREBASE, "test_user"],
            [AllowedIdentityProvider.FIREBASE, "d6c90ea7-c7bd-4963-9d1b-8766c2f41d92"]
        ]
)
def test_identity_new(account_principal_id, provider, subject):
    identity = AccountIdentity.new(principal_id=account_principal_id, subject=subject, provider=provider)
    assert identity.principal_id == account_principal_id
    assert identity.provider == provider
    assert identity.subject == subject

@pytest.mark.parametrize(
        ["provider", "subject"],
        [
            [None, None],
            ["AllowedIdentityProvider.FIREBASE", "test_user"],
            [AllowedIdentityProvider.FIREBASE, None],
            [AllowedIdentityProvider.FIREBASE, 1],
            [AllowedIdentityProvider.FIREBASE, ""],
            [AllowedIdentityProvider.FIREBASE, " "],

        ]
)
def test_identity_new_failure(account_principal_id, provider, subject):
    with pytest.raises(Exception):
        AccountIdentity.new(principal_id=account_principal_id, subject=subject, provider=provider)

def test_indeity_delete(identity):
    identity.delete()
    assert identity.subject == "XXXXXXXXXX"