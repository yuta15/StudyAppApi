from uuid import UUID
from abc import ABC, abstractmethod

from src.app.model.account import AllowedIdentityProvider


class AccountIdentityReadInterface(ABC):
    @abstractmethod
    def resolve_principal_id(self, subject: str, provider: AllowedIdentityProvider) -> UUID | None: ...
