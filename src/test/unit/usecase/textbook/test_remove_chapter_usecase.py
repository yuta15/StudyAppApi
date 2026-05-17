from dataclasses import replace

import pytest

from src.app.core.exceptions import DomainError, UnauthorizedError
from src.app.usecase.textbook.remove_chapter_usecase import RemoveChapterUsecase
from src.test.unit.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_removes_registered_chapter(
    dummy_session,
    positive_modify_textbook_dependencies,
    remove_chapter_dto,
):
    """認可済み著者が登録済みChapterを削除するとTextbookとMetadataが保存されること。"""
    # Arrange
    usecase = RemoveChapterUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Act
    result = usecase.exec(remove_chapter_dto=remove_chapter_dto)

    # Assert
    dependencies = positive_modify_textbook_dependencies
    textbook = dependencies.textbook.input_textbook
    metadata = dependencies.metadata.input_metadata

    assert result is None
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [remove_chapter_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == remove_chapter_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == remove_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook_id == remove_chapter_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == remove_chapter_dto.textbook_id
    assert textbook.chapter_ids == []
    assert metadata.updated_at != metadata.created_at


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_modify_textbook_dependencies,
    remove_chapter_dto,
):
    """Textbook著者認可に失敗した場合、削除対象の取得と保存が実行されないこと。"""
    # Arrange
    usecase = RemoveChapterUsecase(session=dummy_session, dependencies=auth_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(remove_chapter_dto=remove_chapter_dto)

    dependencies = auth_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [remove_chapter_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == remove_chapter_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == remove_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_unregistered_chapter(
    dummy_session,
    positive_modify_textbook_dependencies,
    remove_chapter_dto,
    new_chapter_id,
):
    """未登録Chapterを削除しようとした場合、例外が伝播し保存が実行されないこと。"""
    # Arrange
    unregistered_chapter_dto = replace(remove_chapter_dto, chapter_id=new_chapter_id)
    usecase = RemoveChapterUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Assert
    with pytest.raises(DomainError):
        usecase.exec(remove_chapter_dto=unregistered_chapter_dto)

    dependencies = positive_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook_id == remove_chapter_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == remove_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_modify_textbook_dependencies,
    remove_chapter_dto,
):
    """Textbook保存で例外が発生した場合、例外が伝播しMetadata保存が実行されないこと。"""
    # Arrange
    usecase = RemoveChapterUsecase(session=dummy_session, dependencies=save_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(remove_chapter_dto=remove_chapter_dto)

    dependencies = save_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook is not None
    assert dependencies.metadata.input_metadata is None
