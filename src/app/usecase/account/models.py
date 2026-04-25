from uuid import UUID

from dataclasses import dataclass

from src.app.model.account.entities.value_object import AccountNameStrings, EmailStrings
from src.app.model.account.entities.subjects import AllowedIdentityProvider
from src.app.service.authorization_service.account_auth_read_interface import AccountAuthReadInterface
from src.app.model.account.interface.account_repository_interfaces import (
    AccountRepositoryInterface,
    AccountMetadataRepositoryInterface,
    AccountProfileRepositoryInterface,
    AccountBasicSettingsRepositoryInterface,
    AccountIdentityRepositoryInterface,
)


@dataclass
class CreateAccountDTO:
    account_name:AccountNameStrings
    display_name:str
    email:EmailStrings
    subject:str
    provider:AllowedIdentityProvider


@dataclass
class CreateAccountRepositories:
    account:AccountRepositoryInterface
    metadata:AccountMetadataRepositoryInterface
    profile:AccountProfileRepositoryInterface
    basic_settings:AccountBasicSettingsRepositoryInterface
    identity:AccountIdentityRepositoryInterface


@dataclass
class DeleteAccountRepositories:
    account_auth_read: AccountAuthReadInterface
    account:AccountRepositoryInterface
    metadata:AccountMetadataRepositoryInterface
    profile:AccountProfileRepositoryInterface
    basic_settings:AccountBasicSettingsRepositoryInterface
    identity:AccountIdentityRepositoryInterface