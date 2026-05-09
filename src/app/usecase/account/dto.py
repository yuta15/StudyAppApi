from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

from src.app.model.account import AccountNameStrings, AllowedIdentityProvider, Country, EmailStrings, AccountStatus


@dataclass
class CreateAccountDTO:
    account_name: AccountNameStrings
    display_name: str
    email: EmailStrings
    subject: str
    provider: AllowedIdentityProvider


@dataclass
class ModifyProfile:
    display_name: str | None = None
    email: EmailStrings | None = None
    country: Country | None = None


@dataclass
class ModifyBasicSettings:
    is_public: bool | None = None


@dataclass
class ModifyAccountDTO:
    principal_id: UUID
    profile: ModifyProfile
    basic_settings: ModifyBasicSettings

    def __post_init__(self):
        if isinstance(self.profile, ModifyProfile) and isinstance(self.basic_settings, ModifyBasicSettings):
            return
        raise ValueError("invalid value")


@dataclass
class OutputMetadata:
    created_at: datetime
    last_update: datetime


@dataclass
class OutputProfile:
    display_name: str
    email: EmailStrings
    country: Country


@dataclass
class OutputSettings:
    is_public: bool


@dataclass
class AccountOutputDTO:
    principal_id: UUID
    account_name: AccountNameStrings
    status: AccountStatus
    metadata: OutputMetadata
    profile: OutputProfile
    settings: OutputSettings
