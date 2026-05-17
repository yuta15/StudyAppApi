from dataclasses import replace

import pytest

from src.app.core.exceptions import DomainError, UnauthorizedError
from src.app.usecase.textbook.reorder_chapters_usecase import ReorderChaptersUsecase
from src.test.unit.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_reorders_chapters(
    dummy_session,
    positive_modify_textbook_dependencies,
    reorder_chapters_dto,
    chapter_id,
    another_chapter_id,
):
    """認可済み著者がChapterを並び替えるとTextbookとMetadataが保存されること。"""
    # Arrange
    dependencies = positive_modify_textbook_dependencies
    dependencies.textbook.return_textbook.set_chapters(chapter_ids=[chapter_id, another_chapter_id])
    reordered_chapters_dto = replace(reorder_chapters_dto, chapter_ids=[another_chapter_id, chapter_id])
    usecase = ReorderChaptersUsecase(session=dummy_session, dependencies=dependencies)

    # Act
    result = usecase.exec(reorder_chapters_dto=reordered_chapters_dto)

    # Assert
    textbook = dependencies.textbook.input_textbook
    metadata = dependencies.metadata.input_metadata

    assert result is None
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [reorder_chapters_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == reorder_chapters_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.textbook.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == reorder_chapters_dto.textbook_id
    assert textbook.chapter_ids == [another_chapter_id, chapter_id]
    assert metadata.updated_at != metadata.created_at


def test_exec_success_no_change_skips_save(
    dummy_session,
    positive_modify_textbook_dependencies,
    reorder_chapters_dto,
):
    """現在と同じChapter順を指定した場合、TextbookとMetadataが保存されないこと。"""
    # Arrange
    usecase = ReorderChaptersUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Act
    result = usecase.exec(reorder_chapters_dto=reorder_chapters_dto)

    # Assert
    dependencies = positive_modify_textbook_dependencies
    textbook = dependencies.textbook.return_textbook
    metadata = dependencies.metadata.return_metadata

    assert result is None
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None
    assert textbook.chapter_ids == reorder_chapters_dto.chapter_ids
    assert metadata.updated_at == metadata.created_at


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_modify_textbook_dependencies,
    reorder_chapters_dto,
):
    """Textbook著者認可に失敗した場合、並び替え対象の取得と保存が実行されないこと。"""
    # Arrange
    usecase = ReorderChaptersUsecase(session=dummy_session, dependencies=auth_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(reorder_chapters_dto=reorder_chapters_dto)

    dependencies = auth_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [reorder_chapters_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == reorder_chapters_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_invalid_chapter_ids(
    dummy_session,
    positive_modify_textbook_dependencies,
    reorder_chapters_dto,
    new_chapter_id,
):
    """未登録Chapterを含む並び順を指定した場合、例外が伝播し保存が実行されないこと。"""
    # Arrange
    invalid_reorder_chapters_dto = replace(reorder_chapters_dto, chapter_ids=[new_chapter_id])
    usecase = ReorderChaptersUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Assert
    with pytest.raises(DomainError):
        usecase.exec(reorder_chapters_dto=invalid_reorder_chapters_dto)

    dependencies = positive_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == reorder_chapters_dto.textbook_id
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_modify_textbook_dependencies,
    reorder_chapters_dto,
    chapter_id,
    another_chapter_id,
):
    """Textbook保存で例外が発生した場合、例外が伝播しMetadata保存が実行されないこと。"""
    # Arrange
    dependencies = save_failed_modify_textbook_dependencies
    dependencies.textbook.return_textbook.set_chapters(chapter_ids=[chapter_id, another_chapter_id])
    reordered_chapters_dto = replace(reorder_chapters_dto, chapter_ids=[another_chapter_id, chapter_id])
    usecase = ReorderChaptersUsecase(session=dummy_session, dependencies=dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(reorder_chapters_dto=reordered_chapters_dto)

    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook is not None
    assert dependencies.metadata.input_metadata is None
