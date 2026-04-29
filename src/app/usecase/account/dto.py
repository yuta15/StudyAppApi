from dataclasses import dataclass
from uuid import UUID

from src.app.model.account.entities.value_object import AccountNameStrings, EmailStrings
from src.app.model.account.entities.subjects import AllowedIdentityProvider, Country


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
