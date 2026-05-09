from uuid import UUID

from src.app.core.exceptions import DomainError
from src.app.model.textbook import Chapter, Textbook, TextbookMetadata, TextbookStatus, TitleString
from src.app.model.shared.validation import validate_value_type


class ModifyTextbookDomainService:
    """Textbook集約の変更ルールを管理する。"""

    @staticmethod
    def update_textbook(
        textbook: Textbook,
        metadata: TextbookMetadata,
        title: TitleString | None = None,
        status: TextbookStatus | None = None,
    ) -> bool:
        """教材本体の値を変更し、実際に変更があった場合のみmetadataを更新する。"""
        if title is not None:
            validate_value_type(value=title, valid_type=TitleString)
        if status is not None:
            validate_value_type(value=status, valid_type=TextbookStatus)

        changed = False

        if title is not None and title != textbook.title:
            textbook.set_title(title=title)
            changed = True
        if status is not None and status != textbook.status:
            textbook.set_status(status=status)
            changed = True

        if changed:
            metadata.update()

        return changed

    @staticmethod
    def add_chapter(textbook: Textbook, metadata: TextbookMetadata, title: TitleString) -> Chapter:
        """章を作成し、Textbookの章ID一覧の末尾へ追加する。"""
        chapter = Chapter.new(title=title)
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

        chapter_ids = []
        for registered_id in textbook.chapter_ids:
            if registered_id != chapter_id:
                chapter_ids.append(registered_id)
        textbook.set_chapters(chapter_ids=chapter_ids)
        metadata.update()
        return True

    @staticmethod
    def reorder_chapters(
        textbook: Textbook,
        metadata: TextbookMetadata,
        chapter_ids: list[UUID],
    ) -> bool:
        """登録済みの章ID集合を維持したまま、章の順序だけを変更する。"""
        validate_value_type(value=chapter_ids, valid_type=list)
        for chapter_id in chapter_ids:
            validate_value_type(value=chapter_id, valid_type=UUID)

        if len(chapter_ids) != len(textbook.chapter_ids) or set(chapter_ids) != set(textbook.chapter_ids):
            raise DomainError("Chapter ids must match registered chapters")
        if chapter_ids == textbook.chapter_ids:
            return False

        textbook.set_chapters(chapter_ids=chapter_ids)
        metadata.update()
        return True

    @staticmethod
    def add_author(textbook: Textbook, metadata: TextbookMetadata, author_id: UUID) -> bool:
        """著者を追加し、追加できた場合のみmetadataを更新する。"""
        textbook.add_author(author_id=author_id)
        metadata.update()
        return True

    @staticmethod
    def remove_author(textbook: Textbook, metadata: TextbookMetadata, author_id: UUID) -> bool:
        """著者を削除し、削除できた場合のみmetadataを更新する。"""
        textbook.remove_author(author_id=author_id)
        metadata.update()
        return True
