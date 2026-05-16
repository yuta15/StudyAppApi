from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint
from sqlmodel import Field

from src.app.model.account import AccountStatus, Country, AllowedIdentityProvider
from src.app.schemas.db.base import IncludePrincipalTableBase


class AccountTable(IncludePrincipalTableBase, table=True):
    __tablename__ = "account"

    account_name: str = Field(nullable=False, max_length=128, unique=True)
    status: AccountStatus = Field(nullable=False, index=True)


class AccountMetadataTable(IncludePrincipalTableBase, table=True):
    __tablename__ = "account_metadata"

    created_at: datetime = Field(sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(sa_type=DateTime(timezone=True))
    deleted_at: datetime | None = Field(default=None, index=True, sa_type=DateTime(timezone=True))


class AccountProfileTable(IncludePrincipalTableBase, table=True):
    __tablename__ = "account_profile"

    display_name: str
    email: str
    country: Country


class AccountBasicSettingsTable(IncludePrincipalTableBase, table=True):
    __tablename__ = "account_base_settings"

    is_public: bool


class AccountIdentityTable(IncludePrincipalTableBase, table=True):
    __tablename__ = "account_identity"
    __table_args__ = (UniqueConstraint("provider", "subject", name="uq_account_identity_provider_subject"),)

    subject: str = Field(nullable=False, max_length=255)
    provider: AllowedIdentityProvider = Field(nullable=False)
