from dataclasses import dataclass

from src.app.model.textbook.interface import (
    TextbookRepositoryInterface,
    TextbookMetadataRepositoryInterface,
    TextbookSettingsRepositoryInterface,
)
from src.app.service.domain_read_service.interface.account import AccountAuthReadInterface, AccountReadInterface
from src.app.service.domain_read_service.interface.textbook import TextbookAuthReadInterface, TextbookReadInterface


@dataclass
class CreateTextbookDependencies:
    account_auth_read: AccountAuthReadInterface
    textbook: TextbookRepositoryInterface
    metadata: TextbookMetadataRepositoryInterface
    settings: TextbookSettingsRepositoryInterface


@dataclass
class DeleteTextbookDependencies:
    account_auth_read: AccountAuthReadInterface
    textbook_auth_read: TextbookAuthReadInterface
    textbook: TextbookRepositoryInterface
    metadata: TextbookMetadataRepositoryInterface
    settings: TextbookSettingsRepositoryInterface


@dataclass
class GetTextbookDependencies:
    account_auth_read: AccountAuthReadInterface
    textbook_auth_read: TextbookAuthReadInterface
    account_read: AccountReadInterface
    textbook_read: TextbookReadInterface
