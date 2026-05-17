from abc import ABC, abstractmethod

from src.app.service.interface.identity.model import TokenData


class TokenVerifierInterface(ABC):
    @abstractmethod
    def verify(self, raw_token: str) -> TokenData: ...
