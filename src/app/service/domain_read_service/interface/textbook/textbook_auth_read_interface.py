from abc import ABC, abstractmethod
from uuid import UUID

from src.app.service.domain_read_service.interface.textbook.textbook_read_model import TextbookVisibility


class TextbookAuthReadInterface(ABC):
    @abstractmethod
    def is_author(self, principal_id: UUID, textbook_id: UUID) -> bool:
        """削除されていないかつAuthorにPrincipalIdが含まれていることを確認する。"""
        pass

    @abstractmethod
    def fetch_textbook_visibility(self, textbook_id: UUID) -> TextbookVisibility:
        """
        Textbook公開状態が判定可能な値を返す。
        """
        pass
