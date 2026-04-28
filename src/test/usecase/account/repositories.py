from uuid import UUID

from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.subjects import (
    AccountProfile,
    AccountBasicSettings,
    AccountIdentity
)
from src.app.model.account.interface.account_repository_interfaces import (
    AccountRepositoryInterface,
    AccountMetadataRepositoryInterface,
    AccountProfileRepositoryInterface,
    AccountBasicSettingsRepositoryInterface,
    AccountIdentityRepositoryInterface
)
from src.app.service.authorization_service.account_auth_read_interface import AccountAuthReadInterface


class TestException(Exception):
    """テスト用のダミーエラー"""
    __test__ = False


class TestAccountRepositoryInterface(AccountRepositoryInterface):
    def __init__(self, return_account:Account, is_negative:bool=False):
        self.is_negative = is_negative
        self.return_account = return_account
        self.input_account = None
        self.input_principal_id = None

    def save(self, account:Account) -> Account:
        self.input_account = account
        if self.is_negative:
            raise TestException()
        return account
    
    def get(self, principal_id:UUID) -> Account:
        self.input_principal_id = principal_id
        self.return_account.principal_id = principal_id
        if self.is_negative:
            raise TestException()
        return self.return_account


class TestAccountMetadataInterface(AccountMetadataRepositoryInterface):
    def __init__(self, return_account_metadata:AccountMetadata, is_negative:bool=False):
        self.is_negative = is_negative
        self.return_account_metadata = return_account_metadata
        self.input_metadata = None
        self.input_principal_id = None

    def save(self, metadata:AccountMetadata) -> AccountMetadata:
        self.input_metadata = metadata
        if self.is_negative:
            raise TestException()
        return metadata

    def get(self, principal_id:UUID) -> AccountMetadata:
        self.input_principal_id = principal_id
        self.return_account_metadata.principal_id = principal_id
        return self.return_account_metadata


class TestAccountProfileInterface(AccountProfileRepositoryInterface):
    def __init__(self, return_account_profile:AccountProfile, is_negative:bool=False):
        self.is_negative = is_negative
        self.return_account_profile = return_account_profile
        self.input_profile = None
        self.input_principal_id = None

    def save(self, profile:AccountProfile) -> AccountProfile:
        self.input_profile = profile
        if self.is_negative:
            raise TestException()
        return profile

    def get(self, principal_id:UUID) -> AccountProfile:
        self.input_principal_id = principal_id
        self.return_account_profile.principal_id = principal_id
        if self.is_negative:
            raise TestException()
        return self.return_account_profile



class TestAccountBasicSettingsInterface(AccountBasicSettingsRepositoryInterface):
    def __init__(self, return_account_basic_settings:AccountBasicSettings, is_negative:bool=False):
        self.is_negative = is_negative
        self.return_account_basic_settings = return_account_basic_settings
        self.input_basic_settings = None
        self.input_principal_id = None

    def save(self, basic_settings:AccountBasicSettings) -> AccountBasicSettings:
        self.input_basic_settings = basic_settings
        if self.is_negative:
            raise TestException()
        return basic_settings

    def get(self, principal_id:UUID) -> AccountBasicSettings:
        self.input_principal_id = principal_id
        self.return_account_basic_settings.principal_id = principal_id
        if self.is_negative:
            raise TestException()
        return self.return_account_basic_settings


class TestAccountIdentityInterface(AccountIdentityRepositoryInterface):
    def __init__(self, return_principal_identity:AccountIdentity, is_negative:bool=False):
        self.is_negative = is_negative
        self.return_principal_identity = return_principal_identity
        self.input_identity = None
        self.input_principal_id = None

    def save(self, identity:AccountIdentity) -> AccountIdentity:
        self.input_identity = identity
        if self.is_negative:
            raise TestException()
        return identity

    def get(self, principal_id:UUID) -> AccountIdentity:
        self.input_principal_id = principal_id
        self.return_principal_identity.principal_id = principal_id
        if self.is_negative:
            raise TestException()
        return self.return_principal_identity


class TestAccountAuthReadInterface(AccountAuthReadInterface):
    def __init__(self, auth_result:bool, is_negative:bool=False):
        self.auth_result = auth_result
        self.is_negative = is_negative
        self.input_principal_id = None

    def has_specified_active_user(self, principal_id):
        if self.is_negative:
            raise TestException()
        self.input_principal_id = principal_id
        return self.auth_result
