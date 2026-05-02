from uuid import UUID

from src.app.service.authorization_service.account.account_auth_read_interface import (
    AccountAuthReadInterface,
)
from src.app.core.exceptions import UnauthorizedError


class AccountAuthService:
    def __init__(self, repository: AccountAuthReadInterface):
        self.repository = repository

    def auth(self, principal_id: UUID) -> None:
        result = self.repository.has_specified_active_user(principal_id=principal_id)
        if not result:
            raise UnauthorizedError(
                msg=f"Unauthorized Error principal_id:{principal_id}",
                principal_id=principal_id,
            )
