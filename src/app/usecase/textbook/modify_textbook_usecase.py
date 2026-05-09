from sqlmodel import Session

from src.app.usecase.textbook.dto import ModifyTextbookDTO, OutputTextbookModified, OutputTextbookMetadata
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.app.service.authorization_service.account import AccountAuthService

from src.app.usecase.textbook.dependencies import ModifyTextbookDependencies
from src.app.model.textbook.service import ModifyTextbookDomainService


class ModifyTextbookUsecase:
    def __init__(self, session: Session, dependencies: ModifyTextbookDependencies):
        self._session = session
        self._dependencies = dependencies
        self._textbook_auth = TextbookAuthService(
            account_auth_service=AccountAuthService(repository=dependencies.account_auth_read),
            repository=dependencies.textbook_auth_read,
        )

    def exec(self, modify_textbook_dto: ModifyTextbookDTO) -> OutputTextbookModified:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=modify_textbook_dto.principal_id, textbook_id=modify_textbook_dto.textbook_id
            )

            textbook = self._dependencies.textbook.get(textbook_id=modify_textbook_dto.textbook_id)
            metadata = self._dependencies.metadata.get(textbook_id=modify_textbook_dto.textbook_id)

            is_changed = ModifyTextbookDomainService.update_textbook(
                textbook=textbook, metadata=metadata, title=modify_textbook_dto.title, status=modify_textbook_dto.status
            )

            if is_changed:
                self._dependencies.textbook.save(textbook=textbook)
                self._dependencies.metadata.save(metadata=metadata)

            return OutputTextbookModified(
                textbook_id=textbook.textbook_id,
                title=textbook.title,
                status=textbook.status,
                metadata=OutputTextbookMetadata(created_at=metadata.created_at, updated_at=metadata.updated_at),
            )
