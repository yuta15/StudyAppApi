from uuid import UUID

from src.app.service.interface.account import AccountAuthReadInterface
from src.app.core.exceptions import NotFoundError


class AuthorCheckService:
    def __init__(self, repository: AccountAuthReadInterface):
        self._repository = repository

    def check_active(self, author_id: UUID) -> None:
        is_active = self._repository.has_specified_active_user(principal_id=author_id)
        if not is_active:
            raise NotFoundError(f"Active account not found. account_id: {author_id}")
