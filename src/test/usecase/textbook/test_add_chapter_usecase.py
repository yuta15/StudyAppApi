from uuid import UUID

import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.usecase.textbook.add_chapter_usecase import AddChapterUsecase
from src.test.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_adds_chapter(
    dummy_session,
    positive_add_chapter_dependencies,
    add_chapter_dto,
    chapter_id,
):
    """認可済み著者がChapterを追加するとChapter IDが返り、Textbook、Metadata、Chapterが保存されること。"""
    # Arrange
    usecase = AddChapterUsecase(session=dummy_session, dependencies=positive_add_chapter_dependencies)

    # Act
    added_chapter_id = usecase.exec(add_chapter_dto=add_chapter_dto)

    # Assert
    dependencies = positive_add_chapter_dependencies
    textbook = dependencies.textbook.input_textbook
    metadata = dependencies.metadata.input_metadata
    chapter = dependencies.chapter.input_chapter

    assert isinstance(added_chapter_id, UUID)
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [add_chapter_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == add_chapter_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == add_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook_id == add_chapter_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == add_chapter_dto.textbook_id
    assert chapter.chapter_id == added_chapter_id
    assert chapter.title == add_chapter_dto.chapter_title
    assert chapter.content == ""
    assert textbook.chapter_ids == [chapter_id, added_chapter_id]
    assert metadata.updated_at != metadata.created_at


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_add_chapter_dependencies,
    add_chapter_dto,
):
    """Textbook著者認可に失敗した場合、Chapter作成と保存が実行されないこと。"""
    # Arrange
    usecase = AddChapterUsecase(session=dummy_session, dependencies=auth_failed_add_chapter_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(add_chapter_dto=add_chapter_dto)

    dependencies = auth_failed_add_chapter_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [add_chapter_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == add_chapter_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == add_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None
    assert dependencies.chapter.input_chapter is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_add_chapter_dependencies,
    add_chapter_dto,
):
    """Textbook保存で例外が発生した場合、例外が伝播し後続の保存が実行されないこと。"""
    # Arrange
    usecase = AddChapterUsecase(session=dummy_session, dependencies=save_failed_add_chapter_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(add_chapter_dto=add_chapter_dto)

    dependencies = save_failed_add_chapter_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook is not None
    assert dependencies.metadata.input_metadata is None
    assert dependencies.chapter.input_chapter is None
