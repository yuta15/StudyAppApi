from src.app.core.exceptions import NotFoundError
from src.app.usecase.textbook.dependencies import GetChapterDependencies
from src.app.usecase.textbook.dto import ChapterDTO, GetChapterDTO
from src.app.usecase.textbook.textbook_usecase_base import TextbookUsecaseBase


class GetChapterUsecase(TextbookUsecaseBase[GetChapterDependencies]):
    def exec(self, get_chapter_dto: GetChapterDTO) -> ChapterDTO:
        with self._session.begin():
            self._textbook_auth.auth_read(
                principal_id=get_chapter_dto.principal_id,
                textbook_id=get_chapter_dto.textbook_id,
            )

            textbook = self._dependencies.textbook.get(textbook_id=get_chapter_dto.textbook_id)
            if get_chapter_dto.chapter_id not in textbook.chapter_ids:
                raise NotFoundError(f"Chapter not found chapter_id:{get_chapter_dto.chapter_id}")

            chapter = self._dependencies.chapter.get(chapter_id=get_chapter_dto.chapter_id)

            return ChapterDTO(
                chapter_id=chapter.chapter_id,
                title=chapter.title,
                content=chapter.content,
            )
