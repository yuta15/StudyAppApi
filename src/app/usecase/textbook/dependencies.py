from dataclasses import dataclass

from src.app.model.textbook.interface import (
    ChapterRepositoryInterface,
    TextbookRepositoryInterface,
    TextbookMetadataRepositoryInterface,
    TextbookSettingsRepositoryInterface,
)
from src.app.service.interface.account import AccountAuthReadInterface, AccountReadInterface
from src.app.service.interface.textbook import TextbookAuthReadInterface, TextbookReadInterface


@dataclass
class TextbookAuthDependencies:
    account_auth_read: AccountAuthReadInterface
    textbook_auth_read: TextbookAuthReadInterface


@dataclass
class CreateTextbookDependencies(TextbookAuthDependencies):
    textbook: TextbookRepositoryInterface
    metadata: TextbookMetadataRepositoryInterface
    settings: TextbookSettingsRepositoryInterface


@dataclass
class DeleteTextbookDependencies(TextbookAuthDependencies):
    metadata: TextbookMetadataRepositoryInterface
    settings: TextbookSettingsRepositoryInterface


@dataclass
class ModifyTextbookDependencies(TextbookAuthDependencies):
    textbook: TextbookRepositoryInterface
    metadata: TextbookMetadataRepositoryInterface


@dataclass
class AddChapterDependencies(ModifyTextbookDependencies):
    chapter: ChapterRepositoryInterface


@dataclass
class GetTextbookDependencies(TextbookAuthDependencies):
    account_read: AccountReadInterface
    textbook_read: TextbookReadInterface
