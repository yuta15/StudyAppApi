from abc import ABC, abstractmethod
from typing import TypeVar, Generic


AuthInput = TypeVar("AuthInput")

class AuthServiceBase(ABC, Generic[AuthInput]):
    @abstractmethod
    def is_allowed(self, auth_input:AuthInput) -> bool:...