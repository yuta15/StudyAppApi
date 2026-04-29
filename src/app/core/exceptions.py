from uuid import UUID


class UserOperationError(Exception):
    def __init__(self, msg, principal_id: UUID):
        super().__init__(msg)
        self.principal_id = principal_id


class UnauthorizedError(UserOperationError):
    """認可エラー"""


class DomainError(Exception):
    """ドメイン系のエラー"""
