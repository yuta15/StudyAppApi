from uuid import UUID

from src.app.model.account.value_object.account_settings import AuthSettings, Profile, BasicSettings
from src.app.model.base.enum import Country


def test_new_auth_setting(account_id:UUID, hashed_password:str):
    auth_settings = AuthSettings.new(account_id=account_id, hashed_password=hashed_password)
    assert auth_settings.account_id == account_id
    assert auth_settings.hashed_password == hashed_password

def test_update_password(account_id:UUID, hashed_password:str):
    new_hashed_password = "new_hashed_password"
    auth_settings = AuthSettings.new(account_id=account_id, hashed_password=hashed_password)
    auth_settings.update_hashed_password(new_hashed_password)
    assert auth_settings.hashed_password == new_hashed_password

def test_delete_auth_settings(account_id:UUID, hashed_password:str):
    auth_settings = AuthSettings.new(account_id=account_id, hashed_password=hashed_password)
    auth_settings.delete()
    assert auth_settings.hashed_password is None


def test_new_profile(account_id, email):
    profile = Profile.new(account_id=account_id, email=email)
    assert profile.account_id == account_id
    assert profile.email == email
    assert profile.country is None

def test_update_email(account_id, email):
    updated_email = "new_email@example.com"
    profile = Profile.new(account_id=account_id, email=email)
    profile.update_email(updated_email)
    assert profile.email == updated_email

def test_update_country(account_id, email):
    profile = Profile.new(account_id=account_id, email=email)
    profile.update_country(country=Country.JP)
    assert profile.country == Country.JP

def test_profile_delete(account_id, email):
    profile = Profile.new(account_id=account_id, email=email)
    profile.update_country(country=Country.JP)
    profile.delete()
    assert profile.email is None
    assert profile.country is None


def test_basic_settings(account_id:UUID):
    basic_settings = BasicSettings.new(account_id)
    assert basic_settings.account_id == account_id
    assert basic_settings.is_public == True

def test_update_is_public(account_id:UUID):
    basic_settings = BasicSettings.new(account_id)
    basic_settings.update_public_settings(False)
    assert basic_settings.is_public == False

def test_delete_basic_settings(account_id:UUID):
    basic_settings = BasicSettings.new(account_id)
    basic_settings.delete()
    assert basic_settings.is_public == False