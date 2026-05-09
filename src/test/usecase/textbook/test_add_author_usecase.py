import pytest

from src.app.core.exceptions import NotFoundError, UnauthorizedError
from src.app.usecase.textbook.add_author_usecase import AddAuthorUsecase
from src.test.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_adds_active_author(
    dummy_session,
    positive_modify_textbook_dependencies,
    author_textbook_dto,
):
    """認可済み著者が有効アカウントを著者追加するとTextbookとMetadataが保存されること。"""
    # Arrange
    usecase = AddAuthorUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Act
    usecase.exec(author_textbook_dto=author_textbook_dto)

    # Assert
    dependencies = positive_modify_textbook_dependencies
    textbook = dependencies.textbook.input_textbook
    metadata = dependencies.metadata.input_metadata

    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [
        author_textbook_dto.principal_id,
        author_textbook_dto.author_id,
    ]
    assert dependencies.textbook_auth_read.input_principal_id == author_textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == author_textbook_dto.textbook_id
    assert dependencies.textbook.input_textbook_id == author_textbook_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == author_textbook_dto.textbook_id
    assert textbook.author_ids == [author_textbook_dto.principal_id, author_textbook_dto.author_id]
    assert metadata.updated_at != metadata.created_at


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_modify_textbook_dependencies,
    author_textbook_dto,
):
    """Textbook著者認可に失敗した場合、追加対象チェックと保存が実行されないこと。"""
    # Arrange
    usecase = AddAuthorUsecase(session=dummy_session, dependencies=auth_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(author_textbook_dto=author_textbook_dto)

    dependencies = auth_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [author_textbook_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == author_textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == author_textbook_dto.textbook_id
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_author_not_active(
    dummy_session,
    inactive_author_modify_textbook_dependencies,
    author_textbook_dto,
):
    """追加対象アカウントが有効でない場合、Textbook取得と保存が実行されないこと。"""
    # Arrange
    usecase = AddAuthorUsecase(session=dummy_session, dependencies=inactive_author_modify_textbook_dependencies)

    # Assert
    with pytest.raises(NotFoundError):
        usecase.exec(author_textbook_dto=author_textbook_dto)

    dependencies = inactive_author_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [
        author_textbook_dto.principal_id,
        author_textbook_dto.author_id,
    ]
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_modify_textbook_dependencies,
    author_textbook_dto,
):
    """Textbook保存で例外が発生した場合、例外が伝播しMetadata保存が実行されないこと。"""
    # Arrange
    usecase = AddAuthorUsecase(session=dummy_session, dependencies=save_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(author_textbook_dto=author_textbook_dto)

    dependencies = save_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook is not None
    assert dependencies.metadata.input_metadata is None
