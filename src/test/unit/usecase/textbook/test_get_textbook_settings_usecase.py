import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.usecase.textbook.dto import GetTextbookSettingsOutputDTO
from src.app.usecase.textbook.get_textbook_settings_usecase import GetTextbookSettingsUsecase
from src.test.unit.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_returns_settings(
    dummy_session,
    positive_get_textbook_settings_dependencies,
    textbook_dto,
):
    """認可済み著者がTextbookSettingsを取得できること。"""
    # Arrange
    usecase = GetTextbookSettingsUsecase(
        session=dummy_session,
        dependencies=positive_get_textbook_settings_dependencies,
    )

    # Act
    result = usecase.exec(textbook_dto=textbook_dto)

    # Assert
    dependencies = positive_get_textbook_settings_dependencies
    settings = dependencies.settings.return_settings

    assert isinstance(result, GetTextbookSettingsOutputDTO)
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [textbook_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.settings.input_textbook_id == textbook_dto.textbook_id
    assert result.textbook_id == textbook_dto.textbook_id
    assert result.settings.is_public is settings.is_public


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_get_textbook_settings_dependencies,
    textbook_dto,
):
    """Textbook著者認可に失敗した場合、Settings取得が実行されないこと。"""
    # Arrange
    usecase = GetTextbookSettingsUsecase(
        session=dummy_session,
        dependencies=auth_failed_get_textbook_settings_dependencies,
    )

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(textbook_dto=textbook_dto)

    dependencies = auth_failed_get_textbook_settings_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_ids == [textbook_dto.principal_id]
    assert dependencies.textbook_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.settings.input_textbook_id is None


def test_exec_failure_get_error_propagates(
    dummy_session,
    get_failed_get_textbook_settings_dependencies,
    textbook_dto,
):
    """Settings取得で例外が発生した場合、例外が伝播すること。"""
    # Arrange
    usecase = GetTextbookSettingsUsecase(
        session=dummy_session,
        dependencies=get_failed_get_textbook_settings_dependencies,
    )

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(textbook_dto=textbook_dto)

    dependencies = get_failed_get_textbook_settings_dependencies
    assert dummy_session.is_called
    assert dependencies.settings.input_textbook_id == textbook_dto.textbook_id
