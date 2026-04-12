from uuid import UUID
from abc import ABC, abstractmethod


from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.subjects import (
    AccountProfile,
    AccountBasicSettings
)


class AccountRepositoryInterfaces(ABC):
    @abstractmethod
    def save(self, account:Account) -> Account:...

    @abstractmethod
    def get(self, account_id:UUID) -> Account:...


class AccountMetadataRepositoryInterface(ABC):
    @abstractmethod
    def save(self, metadata:AccountMetadata) -> AccountMetadata:...

    @abstractmethod
    def get(self, account_id:UUID) -> AccountMetadata:...


class AccountProfileRepositoryInterface(ABC):
    @abstractmethod
    def save(self, profile:AccountProfile) -> AccountProfile:...

    @abstractmethod
    def get(self, account_id:UUID) -> AccountProfile:...


class AccountBasicSettingsRepositoryInterface(ABC):
    @abstractmethod
    def save(self, profile:AccountBasicSettings) -> AccountBasicSettings:...

    @abstractmethod
    def get(self, account_id:UUID) -> AccountBasicSettings:...