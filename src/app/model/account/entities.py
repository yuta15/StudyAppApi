from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass
from typing import Self
from uuid import UUID


class AccountSubjcects(Enum):
    ACCOUNT_PROFILE = "ACCOUNT_PROFILE"
    ACCOUNT_BASIC_SETTINGS = "ACCOUNT_BASIC_SETTINGS"
    ACCOUNT_AUTH_SETTINGS = "ACCOUNT_AUTH_SETTINGS"


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    SUSPENDED = "SUSPENDED"


@dataclass
class Metadata:
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime|None = None
    suspended_at:datetime|None = None

    @classmethod
    def new(cls) -> Self:
        utc_now = datetime.now(timezone.utc)
        return Metadata(created_at=utc_now, updated_at=utc_now)

    def to_update(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.updated_at = utc_now

    def to_delete(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.deleted_at = utc_now

    def to_suspend(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.suspended_at = utc_now


@dataclass
class AccountSubject:
    account_id:UUID
    subject_id:UUID


@dataclass
class Account(AccountSubject):
    account_id:UUID
    status:AccountStatus


class AccountAuthorizations(Enum):
    MODIFY = "MODIFY"


@dataclass
class AccountProfile(AccountSubject):
    account_id:UUID
    email:str
    location:str


class AccountProfileAuthorizations(Enum):
    MODIFY = "MODIFY"


@dataclass
class AccountBasicSettings(AccountSubject):
    is_public:bool


class AccountBasicSettingsAuthorizations(Enum):
    MODIFY = "MODIFY"


@dataclass
class AccountAuthSettins(AccountSubject):
    hashed_password:str


class AccountAuthSettinsAuthorizations(Enum):
    MODIFY = "MODIFY"