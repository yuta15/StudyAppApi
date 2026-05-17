from uuid import UUID
from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, UniqueConstraint
from sqlmodel import Field

from src.app.model.account import (
    Account,
    AccountBasicSettings,
    AccountMetadata,
    AccountNameStrings,
    AccountProfile,
    AccountStatus,
    AllowedIdentityProvider,
    Country,
    EmailStrings,
    AccountIdentity,
)
from src.app.schemas.db.base import TableBase


class AccountTable(TableBase, table=True):
    __tablename__ = "account"

    principal_id: UUID = Field(nullable=False, unique=True)
    account_name: str = Field(nullable=False, max_length=128, unique=True)
    status: AccountStatus = Field(nullable=False, index=True)

    @classmethod
    def from_account(cls, account: Account) -> Self:
        return cls(principal_id=account.principal_id, account_name=account.account_name.value, status=account.status)

    def to_account(self) -> Account:
        return Account(
            principal_id=self.principal_id, account_name=AccountNameStrings(value=self.account_name), status=self.status
        )


class AccountMetadataTable(TableBase, table=True):
    __tablename__ = "account_metadata"

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    created_at: datetime = Field(sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(sa_type=DateTime(timezone=True))
    deleted_at: datetime | None = Field(default=None, index=True, sa_type=DateTime(timezone=True))

    @classmethod
    def from_metadata(cls, metadata: AccountMetadata) -> Self:
        return cls(
            principal_id=metadata.principal_id,
            created_at=metadata.created_at,
            updated_at=metadata.updated_at,
            deleted_at=metadata.deleted_at,
        )

    def to_metadata(self) -> AccountMetadata:
        return AccountMetadata(
            principal_id=self.principal_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            deleted_at=self.deleted_at,
        )


class AccountProfileTable(TableBase, table=True):
    __tablename__ = "account_profile"

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    display_name: str
    email: str
    country: Country

    @classmethod
    def from_profile(cls, profile: AccountProfile) -> Self:
        return cls(
            principal_id=profile.principal_id,
            display_name=profile.display_name,
            email=profile.email.value,
            country=profile.country,
        )

    def to_profile(self) -> AccountProfile:
        return AccountProfile(
            principal_id=self.principal_id,
            display_name=self.display_name,
            email=EmailStrings(value=self.email),
            country=self.country,
        )


class AccountBasicSettingsTable(TableBase, table=True):
    __tablename__ = "account_base_settings"

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    is_public: bool

    @classmethod
    def from_basic_settings(cls, basic_settings: AccountBasicSettings) -> Self:
        return cls(
            principal_id=basic_settings.principal_id,
            is_public=basic_settings.is_public,
        )

    def to_basic_settings(self) -> AccountBasicSettings:
        return AccountBasicSettings(
            principal_id=self.principal_id,
            is_public=self.is_public,
        )


class AccountIdentityTable(TableBase, table=True):
    __tablename__ = "account_identity"
    __table_args__ = (UniqueConstraint("provider", "subject", name="uq_account_identity_provider_subject"),)

    principal_id: UUID = Field(nullable=False, unique=True, foreign_key="account.principal_id")
    subject: str = Field(nullable=False, max_length=255)
    provider: AllowedIdentityProvider = Field(nullable=False)

    @classmethod
    def from_identity(cls, identity: AccountIdentity) -> Self:
        return cls(
            principal_id=identity.principal_id,
            subject=identity.subject,
            provider=identity.provider,
        )

    def to_identity(self) -> AccountIdentity:
        return AccountIdentity(
            principal_id=self.principal_id,
            subject=self.subject,
            provider=self.provider,
        )
