from uuid import UUID

from src.test import const
from src.app.model.account.repository.account_repository import AccountRepository
from src.app.model.account.principals.account import Account
from src.app.model.account.value_object.account_settings import Profile, BasicSettings, AuthSettings
from src.app.service.infra.hasher.password_hasher import BasePasswordHasher


class PasswordHasherForTest(BasePasswordHasher):
    def __init__(self):
        self.pasword = None
        self.hashed_password = None
        self.plain_password = None

    def hash(self, password:str) -> str:
        self.pasword = password
        return const.hashed_password

    def verify(self, hashed_password:str, plain_password:str) -> bool:
        self.hashed_password = hashed_password
        self.plain_password = plain_password
        return True


class AccountRepositorySuccess(AccountRepository):
    def __init__(self):
        self.account = None
        self.profile = None
        self.basic_settings = None
        self.auth_settings = None

    def sync_account(self, account:Account) -> Account:
        self.account = account
        return account

    def sync_profile(self, profile:Profile) -> Profile:
        self.profile = profile
        return profile

    def sync_auth_settings(self, auth_settings) -> AuthSettings:
        self.auth_settings = auth_settings
        return auth_settings

    def sync_basic_settings(self, basic_settings:BasicSettings) -> BasicSettings:
        self.basic_settings = basic_settings
        return basic_settings

    def get_account(account_id:UUID) -> Account:...

    def get_profile(account_id:UUID) -> Profile:...

    def get_auth_settings(account_id:UUID) -> AuthSettings:...

    def get_basic_settings(account_id:UUID) -> BasicSettings:...


# TODO:例外投げる系のクラスも作る必要がある