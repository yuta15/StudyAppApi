from uuid import UUID
from abc import ABC, abstractmethod

from src.app.model.account.principals.account import Account
from src.app.model.account.value_object.account_settings import Profile, AuthSettings, BasicSettings


class AccountRepository(ABC):
    @abstractmethod
    def sync_account(self, account:Account) -> Account:...

    @abstractmethod
    def sync_profile(self, profile:Profile) -> Profile:...

    @abstractmethod
    def sync_auth_settings(self, auth_settings) -> AuthSettings:...

    @abstractmethod
    def sync_basic_settings(self, basic_settings:BasicSettings) -> BasicSettings:...

    @abstractmethod
    def get_account(self, account_id:UUID) -> Account:...

    @abstractmethod
    def get_profile(self, account_id:UUID) -> Profile:...

    @abstractmethod
    def get_auth_settings(self, account_id:UUID) -> AuthSettings:...

    @abstractmethod
    def get_basic_settings(self, account_id:UUID) -> BasicSettings:...