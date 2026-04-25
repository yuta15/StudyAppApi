from abc import ABC

from src.app.usecase.account.read_model import ReadAccount


class AccountReadRepository(ABC):
    def get_account(self, principal_id) -> ReadAccount:...
