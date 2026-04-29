from uuid import UUID

from src.app.core.exceptions import DomainError
from src.app.model.shared.validation import validate_value_type
from src.app.model.textbook.entities.metadata import TextbookMetadata
from src.app.model.textbook.entities.subjects import Chapter, Textbook
from src.app.model.textbook.entities.value_object import TitleString


class ModifyTextbookDomainService:
    """Textbook集約の変更ルールを管理する。"""

    @staticmethod
    def update_textbook(
        textbook: Textbook,
        metadata: TextbookMetadata,
        title: TitleString | None = None,
        is_public: bool | None = None,
    ) -> bool:
        """教材本体の値を変更し、実際に変更があった場合のみmetadataを更新する。"""
        if title is not None:
            validate_value_type(value=title, valid_type=TitleString)
        if is_public is not None:
            validate_value_type(value=is_public, valid_type=bool)

        changed = False

        if title is not None and title != textbook.title:
            textbook.set_title(title=title)
            changed = True
        if is_public is not None and is_public != textbook.is_public:
            textbook.set_is_public(is_public=is_public)
            changed = True

        if changed:
            metadata.update()

        return changed

    @staticmethod
    def add_chapter(textbook: Textbook, metadata: TextbookMetadata) -> Chapter:
        """未入力状態の章を作成し、Textbookの章ID一覧の末尾へ追加する。"""
        chapter = Chapter.new()
        textbook.set_chapters(chapter_ids=[*textbook.chapter_ids, chapter.chapter_id])
        metadata.update()
        return chapter

    @staticmethod
    def remove_chapter(
        textbook: Textbook,
        metadata: TextbookMetadata,
        chapter_id: UUID,
    ) -> bool:
        """Textbookから登録済みの章IDを削除し、削除できた場合のみmetadataを更新する。"""
        validate_value_type(value=chapter_id, valid_type=UUID)
        if chapter_id not in textbook.chapter_ids:
            raise DomainError("Chapter is not registered")

        textbook.set_chapters(
            chapter_ids=[registered_id for registered_id in textbook.chapter_ids if registered_id != chapter_id],
        )
        metadata.update()
        return True
