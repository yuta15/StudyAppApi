from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import uuid4

from src.app.model.shared.entities import Principal
from src.app.model.account.entities.value_object import AccountNameStrings
from src.app.model.account.entities.validation import validate_value_type


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    SUSPENDED = "SUSPENDED"


class AccountAuthorizations(Enum):
    MODIFY = "MODIFY"


@dataclass
class Account(Principal):
    """権限を割り当てられる対象"""
    account_name:AccountNameStrings
    status:AccountStatus

    @classmethod
    def new(cls, account_name:AccountNameStrings, **kwargs) -> Self:
        validate_value_type(value=account_name, valid_type=AccountNameStrings)
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

