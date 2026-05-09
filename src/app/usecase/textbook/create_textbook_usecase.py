from uuid import UUID

from sqlmodel import Session

from src.app.usecase.textbook.dto import CreateTextbookDTO
from src.app.model.textbook.service import CreateTextbookInput, CreateTextbookDomainService
from src.app.usecase.textbook.dependencies import CreateTextbookDependencies
from src.app.service.authorization_service.account import AccountAuthService
from src.app.service.authorization_service.textbook import TextbookAuthService


class CreateTextbookUsecase:
    def __init__(self, session: Session, dependencies: CreateTextbookDependencies):
        self._session = session
        self._dependencies = dependencies
        self._textbook_auth = TextbookAuthService(
            account_auth_service=AccountAuthService(repository=dependencies.account_auth_read),
            repository=dependencies.textbook_auth_read,
        )

    def exec(self, create_textbook_dto: CreateTextbookDTO) -> UUID:
        with self._session.begin():
            self._textbook_auth.auth_create(principal_id=create_textbook_dto.principal_id)

            input = CreateTextbookInput(title=create_textbook_dto.title, author_id=create_textbook_dto.principal_id)
            output = CreateTextbookDomainService.exec(create_textbook_input=input)

            self._dependencies.textbook.save(textbook=output.textbook)
            self._dependencies.metadata.save(metadata=output.metadata)
            self._dependencies.settings.save(textbook_settings=output.settings)

        return output.textbook.textbook_id
