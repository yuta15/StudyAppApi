from uuid import UUID

from src.app.model.textbook import Chapter, Textbook, TextbookMetadata, TextbookSettings, TextbookStatus
from src.app.model.textbook.interface import (
    ChapterRepositoryInterface,
    TextbookMetadataRepositoryInterface,
    TextbookRepositoryInterface,
    TextbookSettingsRepositoryInterface,
)
from src.app.service.interface.account import (
    AccountAuthReadInterface,
    AccountReadInterface,
    ReadMinimalAccount,
)
from src.app.service.interface.textbook import (
    TextbookAuthReadInterface,
    TextbookReadInterface,
    TextbookReadModel,
    TextbookVisibility,
)


class TextbookUsecaseTestException(Exception):
    """Textbook usecaseテスト用のダミーエラー"""


class DummyAccountAuthRead(AccountAuthReadInterface):
    def __init__(self, auth_result: bool, is_negative: bool = False, auth_results: list[bool] | None = None):
        self.auth_result = auth_result
        self.auth_results = list(auth_results) if auth_results is not None else None
        self.is_negative = is_negative
        self.input_principal_id = None
        self.input_principal_ids = []

    def has_specified_active_user(self, principal_id: UUID) -> bool:
        self.input_principal_id = principal_id
        self.input_principal_ids.append(principal_id)
        if self.is_negative:
            raise TextbookUsecaseTestException()
        if self.auth_results:
            return self.auth_results.pop(0)
        return self.auth_result


class DummyTextbookAuthRead(TextbookAuthReadInterface):
    def __init__(
        self,
        auth_result: bool,
        is_negative: bool = False,
        is_public: bool = True,
        status: TextbookStatus = TextbookStatus.DRAFT,
    ):
        self.auth_result = auth_result
        self.is_negative = is_negative
        self.is_public = is_public
        self.status = status
        self.input_principal_id = None
        self.input_textbook_id = None
        self.input_visibility_textbook_id = None

    def is_author(self, principal_id: UUID, textbook_id: UUID) -> bool:
        self.input_principal_id = principal_id
        self.input_textbook_id = textbook_id
        if self.is_negative:
            raise TextbookUsecaseTestException()
        return self.auth_result

    def fetch_textbook_visibility(self, textbook_id: UUID) -> TextbookVisibility:
        self.input_visibility_textbook_id = textbook_id
        if self.is_negative:
            raise TextbookUsecaseTestException()
        return TextbookVisibility(
            textbook_id=textbook_id,
            status=self.status,
            is_public=self.is_public,
        )


class DummyTextbookRepository(TextbookRepositoryInterface):
    def __init__(
        self,
        return_textbook: Textbook,
        raise_on_get: bool = False,
        raise_on_save: bool = False,
    ):
        self.return_textbook = return_textbook
        self.raise_on_get = raise_on_get
        self.raise_on_save = raise_on_save
        self.input_textbook = None
        self.input_textbook_id = None

    def save(self, textbook: Textbook) -> Textbook:
        self.input_textbook = textbook
        if self.raise_on_save:
            raise TextbookUsecaseTestException()
        return textbook

    def get(self, textbook_id: UUID) -> Textbook:
        self.input_textbook_id = textbook_id
        if self.raise_on_get:
            raise TextbookUsecaseTestException()
        self.return_textbook.textbook_id = textbook_id
        return self.return_textbook


class DummyTextbookMetadataRepository(TextbookMetadataRepositoryInterface):
    def __init__(
        self,
        return_metadata: TextbookMetadata,
        raise_on_get: bool = False,
        raise_on_save: bool = False,
    ):
        self.return_metadata = return_metadata
        self.raise_on_get = raise_on_get
        self.raise_on_save = raise_on_save
        self.input_metadata = None
        self.input_textbook_id = None

    def save(self, metadata: TextbookMetadata) -> TextbookMetadata:
        self.input_metadata = metadata
        if self.raise_on_save:
            raise TextbookUsecaseTestException()
        return metadata

    def get(self, textbook_id: UUID) -> TextbookMetadata:
        self.input_textbook_id = textbook_id
        if self.raise_on_get:
            raise TextbookUsecaseTestException()
        self.return_metadata.textbook_id = textbook_id
        return self.return_metadata


class DummyChapterRepository(ChapterRepositoryInterface):
    def __init__(
        self,
        return_chapter: Chapter | None = None,
        raise_on_get: bool = False,
        raise_on_save: bool = False,
    ):
        self.return_chapter = return_chapter
        self.raise_on_get = raise_on_get
        self.raise_on_save = raise_on_save
        self.input_chapter = None
        self.input_chapter_id = None

    def save(self, chapter: Chapter) -> Chapter:
        self.input_chapter = chapter
        if self.raise_on_save:
            raise TextbookUsecaseTestException()
        return chapter

    def get(self, chapter_id: UUID) -> Chapter:
        self.input_chapter_id = chapter_id
        if self.raise_on_get or self.return_chapter is None:
            raise TextbookUsecaseTestException()
        self.return_chapter.chapter_id = chapter_id
        return self.return_chapter


class DummyTextbookSettingsRepository(TextbookSettingsRepositoryInterface):
    def __init__(
        self,
        return_settings: TextbookSettings,
        raise_on_get: bool = False,
        raise_on_save: bool = False,
    ):
        self.return_settings = return_settings
        self.raise_on_get = raise_on_get
        self.raise_on_save = raise_on_save
        self.input_textbook_settings = None
        self.input_textbook_id = None

    def save(self, textbook_settings: TextbookSettings) -> TextbookSettings:
        self.input_textbook_settings = textbook_settings
        if self.raise_on_save:
            raise TextbookUsecaseTestException()
        return textbook_settings

    def get(self, textbook_id: UUID) -> TextbookSettings:
        self.input_textbook_id = textbook_id
        if self.raise_on_get:
            raise TextbookUsecaseTestException()
        self.return_settings.textbook_id = textbook_id
        return self.return_settings


class DummyAccountRead(AccountReadInterface):
    def __init__(self, return_accounts: list[ReadMinimalAccount], is_negative: bool = False):
        self.return_accounts = return_accounts
        self.is_negative = is_negative
        self.input_principal_ids = None

    def fetch_minimal_accounts(self, principal_ids: list[UUID]) -> list[ReadMinimalAccount]:
        self.input_principal_ids = principal_ids
        if self.is_negative:
            raise TextbookUsecaseTestException()
        return self.return_accounts


class DummyTextbookRead(TextbookReadInterface):
    def __init__(self, return_textbook: TextbookReadModel, is_negative: bool = False):
        self.return_textbook = return_textbook
        self.is_negative = is_negative
        self.input_textbook_id = None

    def fetch_textbook(self, textbook_id: UUID) -> TextbookReadModel:
        self.input_textbook_id = textbook_id
        if self.is_negative:
            raise TextbookUsecaseTestException()
        return self.return_textbook
