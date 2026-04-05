from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import uuid4

from src.app.model.shared.entities import Principal


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    SUSPENDED = "SUSPENDED"


@dataclass
class Account(Principal):
    """権限を割り当てられる対象"""
    account_name:str
    status:AccountStatus

    @classmethod
    def new(cls, account_name:str, **kwargs) -> Self:
        return Account(
            principal_id=uuid4(),
            account_name=account_name,
            status=AccountStatus.ACTIVE
        )

    def to_delete(self) -> None:
        if self.status == AccountStatus.DELETED:
            raise 
        self.status = AccountStatus.DELETED

    def to_suspended(self) -> None:
        if self.status == AccountStatus.DELETED:
            raise 
        self.status = AccountStatus.SUSPENDED

    def to_active(self) -> None:
        if self.status == AccountStatus.DELETED:
            raise 
        self.status = AccountStatus.ACTIVE

