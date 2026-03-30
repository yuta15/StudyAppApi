from enum import Enum
from uuid import uuid4
from dataclasses import dataclass
from typing import Self

from src.app.model.base.principal import Principal
from src.app.model.account.metadata.account_metadata import AccountMetadata


class AccountStatus(Enum):
    ACTIVE="ACTIVE"
    DELETED="DELETED"
    SUSPENDED="SUSPENDED"


@dataclass
class Account(Principal):
    status:AccountStatus
    metadata:AccountMetadata

    @classmethod
    def new(cls, display_name:str) -> Self:
        return Account(
            principal_id=uuid4(),
            display_name=display_name,
            status=AccountStatus.ACTIVE,
            metadata=AccountMetadata.new()
        )

    def to_delete(self) -> None:
        self.status = AccountStatus.DELETED
        self.metadata.update()

    def to_suspend(self) -> None:
        if not self.status == AccountStatus.DELETED:
            self.status = AccountStatus.SUSPENDED
            self.metadata.update()

    def to_active(self) -> None:
        if not self.status == AccountStatus.DELETED:
            self.status = AccountStatus.ACTIVE
            self.metadata.update()