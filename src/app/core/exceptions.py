from uuid import UUID


class UserOperationError(Exception):
    def __init__(self, msg, principal_id: UUID | None = None):
        super().__init__(msg)
        self.principal_id = principal_id


class UnauthorizedError(UserOperationError):
    """認可エラー"""


class DomainError(Exception):
    """ドメイン系のエラー"""


class NotFoundError(DomainError):
    """存在しない場合のエラー"""


class DatabaseError(Exception):
    """Database系のエラー"""


class DataNotFoundError(Exception):
    """存在しない場合のエラー"""


class InvalidDataError(Exception):
    """不正な値のエラー"""


class NetworkError(Exception):
    """NW系のエラー"""
