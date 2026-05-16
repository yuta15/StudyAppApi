from uuid import UUID

from src.app.model.textbook.service import ModifyTextbookDomainService
from src.app.usecase.textbook.dependencies import AddChapterDependencies
from src.app.usecase.textbook.dto import AddChapterDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class AddChapterUsecase(TextbookUsecaseBase[AddChapterDependencies]):
    def exec(self, add_chapter_dto: AddChapterDTO) -> UUID:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=add_chapter_dto.principal_id,
                textbook_id=add_chapter_dto.textbook_id,
            )
            textbook = self._dependencies.textbook.get(textbook_id=add_chapter_dto.textbook_id)
            metadata = self._dependencies.metadata.get(textbook_id=add_chapter_dto.textbook_id)

            chapter = ModifyTextbookDomainService.add_chapter(
                textbook=textbook,
                metadata=metadata,
                title=add_chapter_dto.chapter_title,
            )

            self._dependencies.textbook.save(textbook=textbook)
            self._dependencies.metadata.save(metadata=metadata)
            self._dependencies.chapter.save(chapter=chapter)

        return chapter.chapter_id
