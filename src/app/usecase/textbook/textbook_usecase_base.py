from typing import Generic, TypeVar

from sqlmodel import Session

from src.app.service.authorization_service.account import AccountAuthService
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.app.usecase.textbook.dependencies import TextbookAuthDependencies

DependenciesT = TypeVar("DependenciesT", bound=TextbookAuthDependencies)


class TextbookUsecaseBase(Generic[DependenciesT]):
    def __init__(self, session: Session, dependencies: DependenciesT):
        self._session = session
        self._dependencies = dependencies
        self._textbook_auth = TextbookAuthService(
            account_auth_service=AccountAuthService(repository=dependencies.account_auth_read),
            repository=dependencies.textbook_auth_read,
        )
