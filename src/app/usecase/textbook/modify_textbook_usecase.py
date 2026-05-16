from src.app.model.textbook.service import ModifyTextbookDomainService
from src.app.usecase.textbook.dependencies import ModifyTextbookDependencies
from src.app.usecase.textbook.dto import ModifyTextbookDTO, OutputTextbookModified, OutputTextbookMetadata
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class ModifyTextbookUsecase(TextbookUsecaseBase[ModifyTextbookDependencies]):
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
