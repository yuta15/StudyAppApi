from uuid import UUID

from src.app.core.exceptions import UnauthorizedError
from src.app.service.authorization_service.account import AccountAuthService
from src.app.service.authorization_service.textbook.textbook_auth_read_interface import (
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

    def auth(self, principal_id: UUID, textbook_id: UUID) -> None:
        self.account_auth_service.auth(principal_id=principal_id)

        is_author = self.repository.is_author(principal_id=principal_id, textbook_id=textbook_id)
        if not is_author:
            raise UnauthorizedError(
                msg=f"Unauthorized Error principal_id:{principal_id}, textbook_id:{textbook_id}",
                principal_id=principal_id,
            )
