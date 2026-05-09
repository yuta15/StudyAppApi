from abc import ABC, abstractmethod

from src.app.service.read_service.account.read_model import ReadAccount


class AccountReadRepository(ABC):
    @abstractmethod
    def get_account(self, principal_id) -> ReadAccount: ...
