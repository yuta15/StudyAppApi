from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.app.core.exceptions import DomainError


def _validate_uuid(value: object, field_name: str) -> None:
    if not isinstance(value, UUID):
        raise ValueError(f"{field_name} must be UUID")


def _validate_title(title: object) -> None:
    if not isinstance(title, str):
        raise ValueError("title must be str")
    if title == "" or title != title.strip():
        raise ValueError("title must not be blank or contain surrounding whitespace")


@dataclass
class Textbook:
    """教材のタイトル、著者、章の並びを管理する。"""

    textbook_id: UUID
    title: str
    author_ids: list[UUID]
    chapter_ids: list[UUID]

    @classmethod
    def new(cls, title: str, author_id: UUID) -> Self:
        """新しい教材を作成する。"""

        _validate_title(title)
        _validate_uuid(author_id, "author_id")
        return cls(
            textbook_id=uuid4(),
            title=title,
            author_ids=[author_id],
            chapter_ids=[],
        )

    def set_title(self, title: str) -> None:
        """教材タイトルを変更する。"""

        _validate_title(title)
        self.title = title

    def add_author(self, author_id: UUID) -> None:
        """著者を追加する。"""

        _validate_uuid(author_id, "author_id")
        if author_id in self.author_ids:
            raise DomainError("Author is already registered")
        self.author_ids.append(author_id)

    def remove_author(self, author_id: UUID) -> None:
        """著者を削除する。"""

        _validate_uuid(author_id, "author_id")
        if author_id not in self.author_ids:
            raise DomainError("Author is not registered")
        if len(self.author_ids) == 1:
            raise DomainError("Textbook must have at least one author")
        self.author_ids.remove(author_id)

    def set_chapters(self, chapter_ids: list[UUID]) -> None:
        """教材に紐づく章 ID の並びを設定する。"""

        if not isinstance(chapter_ids, list):
            raise ValueError("chapter_ids must be list")
        for chapter_id in chapter_ids:
            _validate_uuid(chapter_id, "chapter_id")
        if len(chapter_ids) != len(set(chapter_ids)):
            raise DomainError("Chapter ids must be unique")
        self.chapter_ids = list(chapter_ids)
