from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.app.model.shared.validation import validate_value_type
from src.app.model.textbook.entities.value_object import TitleString


@dataclass
class Chapter:
    """教材の章タイトルとMarkdown形式の本文を管理する。"""

    chapter_id: UUID
    title: TitleString | None = None
    content: str | None = None

    @classmethod
    def new(cls) -> Self:
        """新しい章を作成する。"""
        return cls(chapter_id=uuid4())

    def set_title(self, title: TitleString) -> None:
        """章タイトルを変更する。"""
        validate_value_type(value=title, valid_type=TitleString)
        self.title = title

    def set_content(self, content: str) -> None:
        """章本文を変更する。"""
        validate_value_type(value=content, valid_type=str)
        self.content = content
