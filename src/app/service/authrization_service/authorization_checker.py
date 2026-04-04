from abc import ABC, abstractmethod

from src.app.service.authrization_service.models import TargetAuthorizationUnit


class AuthorizationChecker(ABC):
    @abstractmethod
    def check(self, target:TargetAuthorizationUnit) -> bool:...