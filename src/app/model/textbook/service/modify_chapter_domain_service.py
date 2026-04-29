from src.app.model.shared.validation import validate_value_type
from src.app.model.textbook.entities.metadata import TextbookMetadata
from src.app.model.textbook.entities.subjects import Chapter
from src.app.model.textbook.entities.value_object import TitleString


class ModifyChapterDomainService:
    """Chapterの編集とTextbookMetadataの更新を扱う。"""

    @staticmethod
    def update_chapter(
        chapter: Chapter,
        metadata: TextbookMetadata,
        title: TitleString | None = None,
        content: str | None = None,
    ) -> bool:
        """Chapterに実際の変更がある場合だけ更新し、変更有無を返す。"""
        ModifyChapterDomainService._validate_values(
            title=title,
            content=content,
        )

        changed = False

        if title is not None:
            if title != chapter.title:
                chapter.set_title(title=title)
                changed = True

        if content is not None:
            if content != chapter.content:
                chapter.set_content(content=content)
                changed = True

        if changed:
            metadata.update()

        return changed

    @staticmethod
    def _validate_values(title: TitleString | None = None, content: str | None = None) -> None:
        if title is not None:
            validate_value_type(value=title, valid_type=TitleString)
        if content is not None:
            validate_value_type(value=content, valid_type=str)
