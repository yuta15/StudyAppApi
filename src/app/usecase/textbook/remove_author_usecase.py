from sqlmodel import Session

from src.app.usecase.textbook.dto import AuthorTextbookDTO
from src.app.usecase.textbook.dependencies import ModifyTextbookDependencies
from src.app.model.textbook.service import ModifyTextbookDomainService
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.app.service.authorization_service.account import AccountAuthService


class RemoveAuthorUsecase:
    def __init__(self, session: Session, dependencies: ModifyTextbookDependencies):
        self._session = session
        self._dependencies = dependencies
        self._textbook_auth = TextbookAuthService(
            account_auth_service=AccountAuthService(repository=dependencies.account_auth_read),
            repository=dependencies.textbook_auth_read,
        )

    def exec(self, author_textbook_dto: AuthorTextbookDTO) -> None:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=author_textbook_dto.principal_id, textbook_id=author_textbook_dto.textbook_id
            )

            textbook = self._dependencies.textbook.get(textbook_id=author_textbook_dto.textbook_id)
            metadata = self._dependencies.metadata.get(textbook_id=author_textbook_dto.textbook_id)

            ModifyTextbookDomainService.remove_author(
                textbook=textbook, metadata=metadata, author_id=author_textbook_dto.author_id
            )

            self._dependencies.textbook.save(textbook=textbook)
            self._dependencies.metadata.save(metadata=metadata)
