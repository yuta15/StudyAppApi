from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.app.core.exceptions import DomainError
from src.app.model.shared.validation import validate_value_type
from src.app.model.textbook.entities.value_object import TitleString


@dataclass
class Textbook:
    """教材のタイトル、著者、章の並びを管理する。"""

    textbook_id: UUID
    title: TitleString
    author_ids: list[UUID]
    chapter_ids: list[UUID]

    @classmethod
    def new(cls, title: TitleString, author_id: UUID) -> Self:
        """新しい教材を作成する。"""

        validate_value_type(value=title, valid_type=TitleString)
        validate_value_type(value=author_id, valid_type=UUID)
        return cls(
            textbook_id=uuid4(),
            title=title,
            author_ids=[author_id],
            chapter_ids=[],
        )

    def set_title(self, title: TitleString) -> None:
        """教材タイトルを変更する。"""

        validate_value_type(value=title, valid_type=TitleString)
        self.title = title

    def add_author(self, author_id: UUID) -> None:
        """著者を追加する。"""

        validate_value_type(value=author_id, valid_type=UUID)
        if author_id in self.author_ids:
            raise DomainError("Author is already registered")
        self.author_ids.append(author_id)

    def remove_author(self, author_id: UUID) -> None:
        """著者を削除する。"""

        validate_value_type(value=author_id, valid_type=UUID)
        if author_id not in self.author_ids:
            raise DomainError("Author is not registered")
        if len(self.author_ids) == 1:
            raise DomainError("Textbook must have at least one author")
        self.author_ids.remove(author_id)

    def set_chapters(self, chapter_ids: list[UUID]) -> None:
        """教材に紐づく章 ID の並びを設定する。"""

        validate_value_type(value=chapter_ids, valid_type=list)
        for chapter_id in chapter_ids:
            validate_value_type(value=chapter_id, valid_type=UUID)
        if len(chapter_ids) != len(set(chapter_ids)):
            raise DomainError("Chapter ids must be unique")
        self.chapter_ids = list(chapter_ids)
