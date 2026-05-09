from uuid import UUID
from abc import ABC, abstractmethod

from src.app.service.interface.account.read_model import ReadMinimalAccount


class AccountReadInterface(ABC):
    @abstractmethod
    def fetch_minimal_accounts(self, principal_ids: list[UUID]) -> list[ReadMinimalAccount]: ...
