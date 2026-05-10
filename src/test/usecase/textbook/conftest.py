from datetime import datetime, timezone
from uuid import UUID

import pytest

from src.app.model.account import AccountNameStrings
from src.app.model.textbook import Textbook, TextbookMetadata, TextbookSettings, TextbookStatus, TitleString
from src.app.service.interface.account import ReadMinimalAccount
from src.app.service.interface.textbook import (
    MinimalReadChapter,
    MinimalReadTextbookMetadata,
    TextbookReadModel,
)
from src.app.usecase.textbook.dependencies import (
    AddChapterDependencies,
    CreateTextbookDependencies,
    DeleteTextbookDependencies,
    GetTextbookDependencies,
    ModifyTextbookDependencies,
)
from src.app.usecase.textbook.dto import (
    AddChapterDTO,
    AuthorTextbookDTO,
    CreateTextbookDTO,
    ModifyTextbookDTO,
    RemoveChapterDTO,
    ReorderChaptersDTO,
    TextbookDTO,
)
from src.test import const
from src.test.usecase.textbook.repositories import (
    DummyAccountAuthRead,
    DummyAccountRead,
    DummyChapterRepository,
    DummyTextbookAuthRead,
    DummyTextbookMetadataRepository,
    DummyTextbookRead,
    DummyTextbookRepository,
    DummyTextbookSettingsRepository,
)


@pytest.fixture
def textbook_id():
    return UUID(const.textbook_id)


@pytest.fixture
def textbook_metadata_id():
    return UUID(const.textbook_metadata_id)


@pytest.fixture
def textbook_settings_id():
    return UUID(const.textbook_settings_id)


@pytest.fixture
def second_author_id():
    return UUID(const.textbook_second_author_id)


@pytest.fixture
def chapter_id():
    return UUID(const.textbook_chapter_id)


@pytest.fixture
def another_chapter_id():
    return UUID(const.textbook_another_chapter_id)


@pytest.fixture
def new_chapter_id():
    return UUID(const.textbook_new_chapter_id)


@pytest.fixture
def textbook_title():
    return TitleString(const.textbook_title)


@pytest.fixture
def chapter_title():
    return TitleString(const.textbook_chapter_title)


@pytest.fixture
def textbook(account_principal_id, textbook_id, textbook_title, chapter_id):
    textbook = Textbook.new(title=textbook_title, author_id=account_principal_id)
    textbook.textbook_id = textbook_id
    textbook.set_chapters(chapter_ids=[chapter_id])
    return textbook


@pytest.fixture
def textbook_metadata(textbook_id, textbook_metadata_id):
    utc_now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return TextbookMetadata(
        textbook_id=textbook_id,
        metadata_id=textbook_metadata_id,
        created_at=utc_now,
        updated_at=utc_now,
    )


@pytest.fixture
def textbook_settings(textbook_id, textbook_settings_id):
    return TextbookSettings(
        textbook_id=textbook_id,
        textbook_settings_id=textbook_settings_id,
    )


@pytest.fixture
def create_textbook_dto(account_principal_id, textbook_title):
    return CreateTextbookDTO(
        principal_id=account_principal_id,
        title=textbook_title,
    )


@pytest.fixture
def textbook_dto(account_principal_id, textbook_id):
    return TextbookDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
    )


@pytest.fixture
def modify_textbook_dto(account_principal_id, textbook_id):
    return ModifyTextbookDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
        status=TextbookStatus.PUBLISHED,
    )


@pytest.fixture
def no_change_modify_textbook_dto(account_principal_id, textbook_id):
    return ModifyTextbookDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
    )


@pytest.fixture
def author_textbook_dto(account_principal_id, textbook_id, second_author_id):
    return AuthorTextbookDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
        author_id=second_author_id,
    )


@pytest.fixture
def add_chapter_dto(account_principal_id, textbook_id, chapter_title):
    return AddChapterDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
        chapter_title=chapter_title,
    )


@pytest.fixture
def remove_chapter_dto(account_principal_id, textbook_id, chapter_id):
    return RemoveChapterDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
        chapter_id=chapter_id,
    )


@pytest.fixture
def reorder_chapters_dto(account_principal_id, textbook_id, chapter_id):
    return ReorderChaptersDTO(
        principal_id=account_principal_id,
        textbook_id=textbook_id,
        chapter_ids=[chapter_id],
    )


@pytest.fixture
def read_textbook_model(textbook_id, textbook_title, account_principal_id, second_author_id, chapter_id, chapter_title):
    utc_now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return TextbookReadModel(
        textbook_id=textbook_id,
        title=textbook_title,
        status=TextbookStatus.DRAFT,
        author_ids=[account_principal_id, second_author_id],
        chapters=[MinimalReadChapter(chapter_id=chapter_id, title=chapter_title)],
        metadata=MinimalReadTextbookMetadata(created_at=utc_now, updated_at=utc_now),
    )


@pytest.fixture
def minimal_accounts(account_principal_id, account_name, second_author_id):
    return [
        ReadMinimalAccount(principal_id=account_principal_id, account_name=account_name),
        ReadMinimalAccount(
            principal_id=second_author_id,
            account_name=AccountNameStrings(const.textbook_second_author_account_name),
        ),
    ]


@pytest.fixture
def positive_create_textbook_dependencies(textbook, textbook_metadata, textbook_settings):
    return CreateTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        settings=DummyTextbookSettingsRepository(return_settings=textbook_settings),
    )


@pytest.fixture
def auth_failed_create_textbook_dependencies(textbook, textbook_metadata, textbook_settings):
    return CreateTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=False),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        settings=DummyTextbookSettingsRepository(return_settings=textbook_settings),
    )


@pytest.fixture
def save_failed_create_textbook_dependencies(textbook, textbook_metadata, textbook_settings):
    return CreateTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook, raise_on_save=True),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        settings=DummyTextbookSettingsRepository(return_settings=textbook_settings),
    )


@pytest.fixture
def positive_delete_textbook_dependencies(textbook_metadata, textbook_settings):
    return DeleteTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        settings=DummyTextbookSettingsRepository(return_settings=textbook_settings),
    )


@pytest.fixture
def auth_failed_delete_textbook_dependencies(textbook_metadata, textbook_settings):
    return DeleteTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=False),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        settings=DummyTextbookSettingsRepository(return_settings=textbook_settings),
    )


@pytest.fixture
def get_failed_delete_textbook_dependencies(textbook_metadata, textbook_settings):
    return DeleteTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata, raise_on_get=True),
        settings=DummyTextbookSettingsRepository(return_settings=textbook_settings),
    )


@pytest.fixture
def positive_modify_textbook_dependencies(textbook, textbook_metadata):
    return ModifyTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
    )


@pytest.fixture
def auth_failed_modify_textbook_dependencies(textbook, textbook_metadata):
    return ModifyTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=False),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
    )


@pytest.fixture
def inactive_author_modify_textbook_dependencies(textbook, textbook_metadata):
    return ModifyTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True, auth_results=[True, False]),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
    )


@pytest.fixture
def save_failed_modify_textbook_dependencies(textbook, textbook_metadata):
    return ModifyTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook, raise_on_save=True),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
    )


@pytest.fixture
def positive_add_chapter_dependencies(textbook, textbook_metadata):
    return AddChapterDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        chapter=DummyChapterRepository(),
    )


@pytest.fixture
def auth_failed_add_chapter_dependencies(textbook, textbook_metadata):
    return AddChapterDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=False),
        textbook=DummyTextbookRepository(return_textbook=textbook),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        chapter=DummyChapterRepository(),
    )


@pytest.fixture
def save_failed_add_chapter_dependencies(textbook, textbook_metadata):
    return AddChapterDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        textbook=DummyTextbookRepository(return_textbook=textbook, raise_on_save=True),
        metadata=DummyTextbookMetadataRepository(return_metadata=textbook_metadata),
        chapter=DummyChapterRepository(),
    )


@pytest.fixture
def positive_get_textbook_dependencies(read_textbook_model, minimal_accounts):
    return GetTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        account_read=DummyAccountRead(return_accounts=minimal_accounts),
        textbook_read=DummyTextbookRead(return_textbook=read_textbook_model),
    )


@pytest.fixture
def public_get_textbook_dependencies(read_textbook_model, minimal_accounts):
    return GetTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=False),
        textbook_auth_read=DummyTextbookAuthRead(
            auth_result=False,
            is_public=True,
            status=TextbookStatus.PUBLISHED,
        ),
        account_read=DummyAccountRead(return_accounts=minimal_accounts),
        textbook_read=DummyTextbookRead(return_textbook=read_textbook_model),
    )


@pytest.fixture
def auth_failed_get_textbook_dependencies(read_textbook_model, minimal_accounts):
    return GetTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=False),
        account_read=DummyAccountRead(return_accounts=minimal_accounts),
        textbook_read=DummyTextbookRead(return_textbook=read_textbook_model),
    )


@pytest.fixture
def read_failed_get_textbook_dependencies(read_textbook_model, minimal_accounts):
    return GetTextbookDependencies(
        account_auth_read=DummyAccountAuthRead(auth_result=True),
        textbook_auth_read=DummyTextbookAuthRead(auth_result=True),
        account_read=DummyAccountRead(return_accounts=minimal_accounts),
        textbook_read=DummyTextbookRead(return_textbook=read_textbook_model, is_negative=True),
    )
