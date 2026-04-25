from uuid import UUID
from abc import ABC, abstractmethod


class AuthServiceBase(ABC, ):
    @abstractmethod
    def auth(self, principal_id:UUID) -> None:...