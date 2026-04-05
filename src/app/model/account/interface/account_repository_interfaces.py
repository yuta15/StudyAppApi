from uuid import UUID
from abc import ABC, abstractmethod
from typing import Generic, TypeVar


from src.app.model.account.entities.metadata import AccountMetadata
from src.app.model.account.entities.principals import Account
from src.app.model.account.entities.subjects import AccountSubject



Subject = TypeVar("Subject", bound=AccountSubject)


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


class AccountSubjectRepositoryInterface(ABC, Generic[Subject]):
    @abstractmethod
    def save(self, subject:Subject) -> Subject:...

    @abstractmethod
    def get(self, account_id:UUID) -> Subject:...