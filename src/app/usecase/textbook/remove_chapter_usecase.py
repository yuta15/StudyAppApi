from src.app.model.textbook.service import ModifyTextbookDomainService
from src.app.usecase.textbook.dependencies import ModifyTextbookDependencies
from src.app.usecase.textbook.dto import RemoveChapterDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class RemoveChapterUsecase(TextbookUsecaseBase[ModifyTextbookDependencies]):
    def exec(self, remove_chapter_dto: RemoveChapterDTO) -> None:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=remove_chapter_dto.principal_id,
                textbook_id=remove_chapter_dto.textbook_id,
            )
            textbook = self._dependencies.textbook.get(textbook_id=remove_chapter_dto.textbook_id)
            metadata = self._dependencies.metadata.get(textbook_id=remove_chapter_dto.textbook_id)

            ModifyTextbookDomainService.remove_chapter(
                textbook=textbook,
                metadata=metadata,
                chapter_id=remove_chapter_dto.chapter_id,
            )

            self._dependencies.textbook.save(textbook=textbook)
            self._dependencies.metadata.save(metadata=metadata)
