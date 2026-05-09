from abc import ABC, abstractmethod
from uuid import UUID


class AccountAuthReadInterface(ABC):
    @abstractmethod
    def has_specified_active_user(self, principal_id: UUID) -> bool: ...
