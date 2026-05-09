from dataclasses import dataclass

from src.app.model.account.interface.account_repository_interfaces import (
    AccountRepositoryInterface,
    AccountMetadataRepositoryInterface,
    AccountProfileRepositoryInterface,
    AccountBasicSettingsRepositoryInterface,
    AccountIdentityRepositoryInterface,
)
from src.app.service.interface.account import AccountAuthReadInterface


@dataclass
class CreateAccountRepositories:
    account: AccountRepositoryInterface
    metadata: AccountMetadataRepositoryInterface
    profile: AccountProfileRepositoryInterface
    basic_settings: AccountBasicSettingsRepositoryInterface
    identity: AccountIdentityRepositoryInterface


@dataclass
class DeleteAccountRepositories:
    account_auth_read: AccountAuthReadInterface
    account: AccountRepositoryInterface
    metadata: AccountMetadataRepositoryInterface
    profile: AccountProfileRepositoryInterface
    basic_settings: AccountBasicSettingsRepositoryInterface
    identity: AccountIdentityRepositoryInterface


@dataclass
class ModifyAccountRepositories:
    account_auth_read: AccountAuthReadInterface
    account: AccountRepositoryInterface
    metadata: AccountMetadataRepositoryInterface
    profile: AccountProfileRepositoryInterface
    basic_settings: AccountBasicSettingsRepositoryInterface
