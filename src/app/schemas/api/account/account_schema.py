from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from src.app.model.account import AccountStatus, AllowedIdentityProvider, Country
from src.app.schemas.api.base import ApiModel


class BaseAccountInput(ApiModel):
    id: UUID


class CreateAccountInput(ApiModel):
    account_name: str
    display_name: str
    email: EmailStr
    subject: str
    provider: AllowedIdentityProvider


class CreateAccountOutput(ApiModel):
    id: UUID


class ModifyAccountProfileInput(ApiModel):
    display_name: str | None = None
    email: EmailStr | None = None
    country: Country | None = None


class ModifyAccountBasicSettingsInput(ApiModel):
    is_public: bool | None = None


class ModifyAccountInput(ApiModel):
    profile: ModifyAccountProfileInput = Field(default_factory=ModifyAccountProfileInput)
    basic_settings: ModifyAccountBasicSettingsInput = Field(default_factory=ModifyAccountBasicSettingsInput)


class AccountMetadataOutput(ApiModel):
    created_at: datetime
    last_update: datetime


class AccountProfileOutput(ApiModel):
    display_name: str
    email: EmailStr
    country: Country


class AccountSettingsOutput(ApiModel):
    is_public: bool


class AccountOutput(ApiModel):
    principal_id: UUID
    account_name: str
    status: AccountStatus
    metadata: AccountMetadataOutput
    profile: AccountProfileOutput
    settings: AccountSettingsOutput
