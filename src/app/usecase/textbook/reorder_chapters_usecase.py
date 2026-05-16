from src.app.model.textbook.service import ModifyTextbookDomainService
from src.app.usecase.textbook.dependencies import ModifyTextbookDependencies
from src.app.usecase.textbook.dto import ReorderChaptersDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class ReorderChaptersUsecase(TextbookUsecaseBase[ModifyTextbookDependencies]):
    def exec(self, reorder_chapters_dto: ReorderChaptersDTO) -> None:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=reorder_chapters_dto.principal_id, textbook_id=reorder_chapters_dto.textbook_id
            )

            textbook = self._dependencies.textbook.get(textbook_id=reorder_chapters_dto.textbook_id)
            metadata = self._dependencies.metadata.get(textbook_id=reorder_chapters_dto.textbook_id)

            is_reorder = ModifyTextbookDomainService.reorder_chapters(
                textbook=textbook, metadata=metadata, chapter_ids=reorder_chapters_dto.chapter_ids
            )

            if is_reorder:
                self._dependencies.textbook.save(textbook=textbook)
                self._dependencies.metadata.save(metadata=metadata)
