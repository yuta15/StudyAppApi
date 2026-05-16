from uuid import UUID
from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint
from sqlmodel import Field

from src.app.model.account import AccountStatus, Country, AllowedIdentityProvider
from src.app.schemas.db.base import TableBase


class AccountTable(TableBase, table=True):
    __tablename__ = "account"

    principal_id: UUID = Field(nullable=False, unique=True)
    account_name: str = Field(nullable=False, max_length=128, unique=True)
    status: AccountStatus = Field(nullable=False, index=True)


class AccountMetadataTable(TableBase, table=True):
    __tablename__ = "account_metadata"

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    created_at: datetime = Field(sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(sa_type=DateTime(timezone=True))
    deleted_at: datetime | None = Field(default=None, index=True, sa_type=DateTime(timezone=True))


class AccountProfileTable(TableBase, table=True):
    __tablename__ = "account_profile"

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    display_name: str
    email: str
    country: Country


class AccountBasicSettingsTable(TableBase, table=True):
    __tablename__ = "account_base_settings"

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    is_public: bool


class AccountIdentityTable(TableBase, table=True):
    __tablename__ = "account_identity"
    __table_args__ = (UniqueConstraint("provider", "subject", name="uq_account_identity_provider_subject"),)

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    subject: str = Field(nullable=False, max_length=255)
    provider: AllowedIdentityProvider = Field(nullable=False)
