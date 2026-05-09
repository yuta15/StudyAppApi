from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from src.app.model.shared.validation import validate_value_type


@dataclass
class TextbookSettings:
    """教材の公開設定を管理する。"""

    textbook_id: UUID
    textbook_settings_id: UUID
    is_public: bool = True

    @classmethod
    def new(cls, textbook_id: UUID) -> Self:
        """新しい教材設定を作成する。"""
        validate_value_type(value=textbook_id, valid_type=UUID)
        return cls(
            textbook_id=textbook_id,
            textbook_settings_id=uuid4(),
        )

    def set_is_public(self, is_public: bool) -> None:
        """教材設定の公開状態を変更する。"""
        validate_value_type(value=is_public, valid_type=bool)
        self.is_public = is_public

    def delete(self) -> None:
        """教材設定を削除状態にする。"""
        self.is_public = False
