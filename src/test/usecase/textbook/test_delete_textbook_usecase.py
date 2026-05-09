from datetime import datetime

import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.usecase.textbook.delete_textbook_usecase import DeleteTextbookUsecase
from src.test.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_deletes_textbook(dummy_session, positive_delete_textbook_dependencies, textbook_dto):
    """認可済み著者が教材を削除するとMetadataとSettingsが削除状態で保存されること。"""
    # Arrange
    usecase = DeleteTextbookUsecase(session=dummy_session, dependencies=positive_delete_textbook_dependencies)

    # Act
    usecase.exec(textbook_dto=textbook_dto)

    # Assert
    dependencies = positive_delete_textbook_dependencies
    metadata = dependencies.metadata.input_metadata
    settings = dependencies.settings.input_textbook_settings

    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.settings.input_textbook_id == textbook_dto.textbook_id
    assert metadata.textbook_id == textbook_dto.textbook_id
    assert isinstance(metadata.deleted_at, datetime)
    assert settings.textbook_id == textbook_dto.textbook_id
    assert settings.is_public is False


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_delete_textbook_dependencies,
    textbook_dto,
):
    """Textbook著者認可に失敗した場合、削除対象の取得と保存が実行されないこと。"""
    # Arrange
    usecase = DeleteTextbookUsecase(session=dummy_session, dependencies=auth_failed_delete_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(textbook_dto=textbook_dto)

    dependencies = auth_failed_delete_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_id == textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.settings.input_textbook_id is None
    assert dependencies.metadata.input_metadata is None
    assert dependencies.settings.input_textbook_settings is None


def test_exec_failure_get_error_propagates(
    dummy_session,
    get_failed_delete_textbook_dependencies,
    textbook_dto,
):
    """削除対象Metadataの取得で例外が発生した場合、例外が伝播し保存が実行されないこと。"""
    # Arrange
    usecase = DeleteTextbookUsecase(session=dummy_session, dependencies=get_failed_delete_textbook_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(textbook_dto=textbook_dto)

    dependencies = get_failed_delete_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.metadata.input_textbook_id == textbook_dto.textbook_id
    assert dependencies.settings.input_textbook_id is None
    assert dependencies.metadata.input_metadata is None
    assert dependencies.settings.input_textbook_settings is None
