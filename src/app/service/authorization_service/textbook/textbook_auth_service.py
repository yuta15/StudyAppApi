from uuid import UUID

from src.app.core.exceptions import UnauthorizedError
from src.app.service.authorization_service.account import AccountAuthService
from src.app.model.textbook import TextbookStatus
from src.app.service.interface.textbook.textbook_auth_read_interface import (
    TextbookAuthReadInterface,
)


class TextbookAuthService:
    """Textbook関連操作の認可を行う。"""

    def __init__(
        self,
        account_auth_service: AccountAuthService,
        repository: TextbookAuthReadInterface,
    ):
        self.account_auth_service = account_auth_service
        self.repository = repository

    def auth_create(self, principal_id: UUID) -> None:
        self.account_auth_service.auth(principal_id=principal_id)

    def auth_manage(self, principal_id: UUID, textbook_id: UUID) -> None:
        self._auth_author(principal_id=principal_id, textbook_id=textbook_id)

    def auth_read(self, principal_id: UUID | None, textbook_id: UUID) -> None:
        # 著者以外はis_publicかつStatusがPUBLISHEDのものだけが閲覧可能
        is_publicly_readable = self._is_publicly_readable(textbook_id=textbook_id)
        if is_publicly_readable:
            return
        # 著者用の認可
        self._auth_author(principal_id=principal_id, textbook_id=textbook_id)

    def _auth_author(self, principal_id: UUID | None, textbook_id: UUID) -> None:
        if principal_id is None:
            raise UnauthorizedError(msg=f"Unauthorized Error textbook_id:{textbook_id}")
        self.account_auth_service.auth(principal_id=principal_id)
        is_author = self.repository.is_author(principal_id=principal_id, textbook_id=textbook_id)
        if not is_author:
            raise UnauthorizedError(
                msg=f"Unauthorized Error principal_id:{principal_id}, textbook_id:{textbook_id}",
                principal_id=principal_id,
            )

    def _is_publicly_readable(self, textbook_id: UUID) -> bool:
        """
        全てのユーザーが触れる状態か判定する。
        """
        textbook_visibility = self.repository.fetch_textbook_visibility(textbook_id=textbook_id)
        return textbook_visibility.is_public and textbook_visibility.status == TextbookStatus.PUBLISHED
