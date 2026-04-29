from datetime import datetime
from uuid import UUID
from dataclasses import dataclass

from src.app.model.account.entities.value_object import EmailStrings, AccountNameStrings
from src.app.model.account.entities.subjects import Country
from src.app.model.account.entities.principals import AccountStatus


@dataclass
class ReadMetadata:
    created_at: datetime
    last_update: datetime


@dataclass
class ReadProfile:
    display_name: str
    email: EmailStrings
    country: Country


@dataclass
class ReadSettings:
    is_public: bool


@dataclass
class ReadAccount:
    principal_id: UUID
    account_name: AccountNameStrings
    status: AccountStatus
    metadata: ReadMetadata
    profile: ReadProfile
    settings: ReadSettings
