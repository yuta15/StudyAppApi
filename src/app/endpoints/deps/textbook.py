from fastapi import Depends
from sqlmodel import Session

from src.app.endpoints.deps.db import get_session
from src.app.infra.account import AccountReadRepository
from src.app.infra.auth import AccountAuthReadRepository, TextbookAuthReadRepository
from src.app.infra.textbook import (
    ChapterRepository,
    TextbookMetadataRepository,
    TextbookReadRepository,
    TextbookRepository,
    TextbookSettingsRepository,
)
from src.app.usecase.textbook.dependencies import (
    AddChapterDependencies,
    CreateTextbookDependencies,
    DeleteTextbookDependencies,
    GetTextbookDependencies,
    ModifyChapterDependencies,
    ModifyTextbookDependencies,
    ModifyTextbookSettingsDependencies,
    GetChapterDependencies,
    GetTextbookSettingsDependencies,
)


def get_create_textbook_dependencies(session: Session = Depends(get_session)) -> CreateTextbookDependencies:
    return CreateTextbookDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        textbook=TextbookRepository(session=session),
        metadata=TextbookMetadataRepository(session=session),
        settings=TextbookSettingsRepository(session=session),
    )


def get_get_textbook_dependencies(session: Session = Depends(get_session)) -> GetTextbookDependencies:
    return GetTextbookDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        account_read=AccountReadRepository(session=session),
        textbook_read=TextbookReadRepository(session=session),
    )


def get_modify_textbook_dependencies(session: Session = Depends(get_session)) -> ModifyTextbookDependencies:
    return ModifyTextbookDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        textbook=TextbookRepository(session=session),
        metadata=TextbookMetadataRepository(session=session),
    )


def get_delete_textbook_dependencies(session: Session = Depends(get_session)) -> DeleteTextbookDependencies:
    return DeleteTextbookDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        metadata=TextbookMetadataRepository(session=session),
        settings=TextbookSettingsRepository(session=session),
    )


def get_add_chapter_dependencies(session: Session = Depends(get_session)) -> AddChapterDependencies:
    return AddChapterDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        textbook=TextbookRepository(session=session),
        metadata=TextbookMetadataRepository(session=session),
        chapter=ChapterRepository(session=session),
    )


def get_modify_chapter_dependencies(session: Session = Depends(get_session)) -> ModifyChapterDependencies:
    return ModifyChapterDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        textbook=TextbookRepository(session=session),
        metadata=TextbookMetadataRepository(session=session),
        chapter=ChapterRepository(session=session),
    )


def get_get_chapter_dependencies(session: Session = Depends(get_session)) -> GetChapterDependencies:
    return GetChapterDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        textbook=TextbookRepository(session=session),
        chapter=ChapterRepository(session=session),
    )


def get_modify_textbook_settings_dependencies(
    session: Session = Depends(get_session),
) -> ModifyTextbookSettingsDependencies:
    return ModifyTextbookSettingsDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        metadata=TextbookMetadataRepository(session=session),
        settings=TextbookSettingsRepository(session=session),
    )


def get_get_textbook_settings_dependencies(
    session: Session = Depends(get_session),
) -> GetTextbookSettingsDependencies:
    return GetTextbookSettingsDependencies(
        account_auth_read=AccountAuthReadRepository(session=session),
        textbook_auth_read=TextbookAuthReadRepository(session=session),
        settings=TextbookSettingsRepository(session=session),
    )
