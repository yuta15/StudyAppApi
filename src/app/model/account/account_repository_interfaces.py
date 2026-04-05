from uuid import UUID
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.app.model.account.aggregate import AccountAggregate
from src.app.model.account.entities import Account
from src.app.model.account.account_subjects import AccountSubject


Subject = TypeVar("Subject", bound=AccountSubject)

class AccountAggregateRepositoryInterface(ABC):
    @abstractmethod
    def save(self, aggregate:AccountAggregate) -> AccountAggregate:...

    @abstractmethod
    def get(self, account_id:UUID) -> AccountAggregate:...


class AccountRepositoryInterfaces(ABC):
    @abstractmethod
    def save(self, account:Account) -> Account:...

    @abstractmethod
    def get(self, account_id:UUID) -> Account:...


class AccountSubjectRepositoryInterface(ABC, Generic[Subject]):
    @abstractmethod
    def save(self, subject:Subject) -> Subject:...

    @abstractmethod
    def get(self, account_id:UUID) -> Subject:...