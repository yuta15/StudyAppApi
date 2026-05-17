import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.service.domain_read_service.textbook import ReadTextbookDetailsModel
from src.app.usecase.textbook.get_textbook_usecase import GetTextbookUsecase
from src.test.unit.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_gets_textbook_details(dummy_session, positive_get_textbook_dependencies, textbook_dto):
    """認可済み著者が教材詳細を取得すると教材と著者のReadModelが結合されて返ること。"""
    # Arrange
    usecase = GetTextbookUsecase(session=dummy_session, dependencies=positive_get_textbook_dependencies)

    # Act
    result = usecase.exec(textbook_dto=textbook_dto)

    # Assert
    dependencies = positive_get_textbook_dependencies
    textbook = dependencies.textbook_read.return_textbook
    authors = dependencies.account_read.return_accounts

    assert isinstance(result, ReadTextbookDetailsModel)
    assert dummy_session.is_called
    assert dependencies.textbook_auth_read.input_visibility_textbook_id == textbook_dto.textbook_id
    assert dependencies.account_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.textbook_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.account_read.input_principal_ids == textbook.author_ids
    assert result.textbook_id == textbook.textbook_id
    assert result.title == textbook.title
    assert result.status == textbook.status
    assert result.authors == authors
    assert result.chapters == textbook.chapters
    assert result.metadata == textbook.metadata


def test_exec_success_gets_public_textbook_details_without_author_auth(
    dummy_session,
    public_get_textbook_dependencies,
    textbook_dto,
):
    """公開済み教材の場合、著者認可なしで教材詳細が取得できること。"""
    # Arrange
    usecase = GetTextbookUsecase(session=dummy_session, dependencies=public_get_textbook_dependencies)

    # Act
    result = usecase.exec(textbook_dto=textbook_dto)

    # Assert
    dependencies = public_get_textbook_dependencies
    textbook = dependencies.textbook_read.return_textbook

    assert isinstance(result, ReadTextbookDetailsModel)
    assert dummy_session.is_called
    assert dependencies.textbook_auth_read.input_visibility_textbook_id == textbook_dto.textbook_id
    assert dependencies.account_auth_read.input_principal_id is None
    assert dependencies.textbook_auth_read.input_principal_id is None
    assert dependencies.textbook_auth_read.input_textbook_id is None
    assert dependencies.textbook_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.account_read.input_principal_ids == textbook.author_ids
    assert result.textbook_id == textbook.textbook_id
    assert result.metadata == textbook.metadata


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_get_textbook_dependencies,
    textbook_dto,
):
    """Textbook著者認可に失敗した場合、ReadModel取得が実行されないこと。"""
    # Arrange
    usecase = GetTextbookUsecase(session=dummy_session, dependencies=auth_failed_get_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(textbook_dto=textbook_dto)

    dependencies = auth_failed_get_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook_auth_read.input_visibility_textbook_id == textbook_dto.textbook_id
    assert dependencies.account_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.textbook_read.input_textbook_id is None
    assert dependencies.account_read.input_principal_ids is None


def test_exec_failure_read_error_propagates(
    dummy_session,
    read_failed_get_textbook_dependencies,
    textbook_dto,
):
    """Textbook ReadModel取得で例外が発生した場合、例外が伝播し著者取得が実行されないこと。"""
    # Arrange
    usecase = GetTextbookUsecase(session=dummy_session, dependencies=read_failed_get_textbook_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(textbook_dto=textbook_dto)

    dependencies = read_failed_get_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.account_read.input_principal_ids is None
