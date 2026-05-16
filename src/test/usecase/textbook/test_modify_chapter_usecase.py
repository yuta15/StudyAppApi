from dataclasses import replace

import pytest

from src.app.core.exceptions import NotFoundError, UnauthorizedError
from src.app.usecase.textbook.modify_chapter_usecase import ModifyChapterUsecase
from src.test.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_updates_chapter(
    dummy_session,
    positive_modify_chapter_dependencies,
    modify_chapter_dto,
):
    """認可済み著者がChapterを変更するとChapterとMetadataが保存されること。"""
    # Arrange
    usecase = ModifyChapterUsecase(session=dummy_session, dependencies=positive_modify_chapter_dependencies)

    # Act
    result = usecase.exec(modify_chapter_dto=modify_chapter_dto)

    # Assert
    dependencies = positive_modify_chapter_dependencies
    chapter = dependencies.chapter.input_chapter
    metadata = dependencies.metadata.input_metadata

    assert result is None
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [modify_chapter_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == modify_chapter_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.chapter.input_chapter_id == modify_chapter_dto.chapter_id
    assert dependencies.metadata.input_textbook_id == modify_chapter_dto.textbook_id
    assert chapter.title == modify_chapter_dto.title
    assert chapter.content == modify_chapter_dto.content
    assert metadata.updated_at != metadata.created_at


def test_exec_success_no_change_skips_save(
    dummy_session,
    positive_modify_chapter_dependencies,
    modify_chapter_dto,
):
    """Chapterに変更がない場合、ChapterとMetadataが保存されないこと。"""
    # Arrange
    chapter = positive_modify_chapter_dependencies.chapter.return_chapter
    no_change_modify_chapter_dto = replace(
        modify_chapter_dto,
        title=chapter.title,
        content=chapter.content,
    )
    usecase = ModifyChapterUsecase(session=dummy_session, dependencies=positive_modify_chapter_dependencies)

    # Act
    result = usecase.exec(modify_chapter_dto=no_change_modify_chapter_dto)

    # Assert
    dependencies = positive_modify_chapter_dependencies
    metadata = dependencies.metadata.return_metadata

    assert result is None
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.chapter.input_chapter_id == modify_chapter_dto.chapter_id
    assert dependencies.metadata.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.chapter.input_chapter is None
    assert dependencies.metadata.input_metadata is None
    assert metadata.updated_at == metadata.created_at


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_modify_chapter_dependencies,
    modify_chapter_dto,
):
    """Textbook著者認可に失敗した場合、変更対象の取得と保存が実行されないこと。"""
    # Arrange
    usecase = ModifyChapterUsecase(session=dummy_session, dependencies=auth_failed_modify_chapter_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(modify_chapter_dto=modify_chapter_dto)

    dependencies = auth_failed_modify_chapter_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [modify_chapter_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == modify_chapter_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.chapter.input_chapter_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.chapter.input_chapter is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_unregistered_chapter(
    dummy_session,
    positive_modify_chapter_dependencies,
    modify_chapter_dto,
    new_chapter_id,
):
    """Textbookに未登録のChapterを変更しようとした場合、例外が伝播し保存が実行されないこと。"""
    # Arrange
    unregistered_chapter_dto = replace(modify_chapter_dto, chapter_id=new_chapter_id)
    usecase = ModifyChapterUsecase(session=dummy_session, dependencies=positive_modify_chapter_dependencies)

    # Assert
    with pytest.raises(NotFoundError):
        usecase.exec(modify_chapter_dto=unregistered_chapter_dto)

    dependencies = positive_modify_chapter_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.chapter.input_chapter_id == new_chapter_id
    assert dependencies.metadata.input_textbook_id == modify_chapter_dto.textbook_id
    assert dependencies.chapter.input_chapter is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_modify_chapter_dependencies,
    modify_chapter_dto,
):
    """Chapter保存で例外が発生した場合、例外が伝播しMetadata保存が実行されないこと。"""
    # Arrange
    usecase = ModifyChapterUsecase(session=dummy_session, dependencies=save_failed_modify_chapter_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(modify_chapter_dto=modify_chapter_dto)

    dependencies = save_failed_modify_chapter_dependencies
    assert dummy_session.is_called
    assert dependencies.chapter.input_chapter is not None
    assert dependencies.metadata.input_metadata is None
