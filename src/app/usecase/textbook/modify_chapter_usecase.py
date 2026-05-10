from src.app.core.exceptions import NotFoundError
from src.app.usecase.textbook.dependencies import ModifyChapterDependencies
from src.app.usecase.textbook.dto import ModifyChapterDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase
from src.app.model.textbook.service import ModifyChapterDomainService


class ModifyChapterUsecase(TextbookUsecaseBase[ModifyChapterDependencies]):
    def exec(self, modify_chapter_dto: ModifyChapterDTO) -> None:
        with self._session.begin():
            self._textbook_auth.auth_manage(
                principal_id=modify_chapter_dto.principal_id,
                textbook_id=modify_chapter_dto.textbook_id,
            )

            textbook = self._dependencies.textbook.get(textbook_id=modify_chapter_dto.textbook_id)
            chapter = self._dependencies.chapter.get(chapter_id=modify_chapter_dto.chapter_id)
            metadata = self._dependencies.metadata.get(textbook_id=modify_chapter_dto.textbook_id)

            if modify_chapter_dto.chapter_id not in textbook.chapter_ids:
                raise NotFoundError(f"Chapter not found chapter_id:{modify_chapter_dto.chapter_id}")

            is_changed = ModifyChapterDomainService.update_chapter(
                chapter=chapter, metadata=metadata, title=modify_chapter_dto.title, content=modify_chapter_dto.content
            )

            if is_changed:
                self._dependencies.chapter.save(chapter=chapter)
                self._dependencies.metadata.save(metadata=metadata)
