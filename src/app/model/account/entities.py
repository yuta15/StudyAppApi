from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
from typing import Self
from uuid import uuid4, UUID

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


@dataclass
class AccountMetadata:
    principal_id:UUID
    metadata_id:UUID
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime|None = None

    @classmethod
    def new(cls, principal_id:UUID) -> Self:
        utc_now = datetime.now(timezone.utc)
        return AccountMetadata(
            principal_id=principal_id,
            metadata_id=uuid4(),
            created_at=utc_now,
            updated_at=utc_now
        )

    def update(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.updated_at = utc_now

    def delete(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.deleted_at = utc_now


class AccountAuthorizations(Enum):
    MODIFY = "MODIFY"
