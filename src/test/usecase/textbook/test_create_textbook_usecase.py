from uuid import UUID

import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.model.textbook import TextbookStatus
from src.app.usecase.textbook.create_textbook_usecase import CreateTextbookUsecase
from src.test.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_creates_textbook(dummy_session, positive_create_textbook_dependencies, create_textbook_dto):
    """認可済みユーザーが教材を作成するとTextbook、Metadata、Settingsが保存されること。"""
    # Arrange
    usecase = CreateTextbookUsecase(session=dummy_session, dependencies=positive_create_textbook_dependencies)

    # Act
    textbook_id = usecase.exec(create_textbook_dto=create_textbook_dto)

    # Assert
    dependencies = positive_create_textbook_dependencies
    textbook = dependencies.textbook.input_textbook
    metadata = dependencies.metadata.input_metadata
    settings = dependencies.settings.input_textbook_settings

    assert isinstance(textbook_id, UUID)
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_id == create_textbook_dto.principal_id
    assert textbook.textbook_id == textbook_id
    assert textbook.title == create_textbook_dto.title
    assert textbook.author_ids == [create_textbook_dto.principal_id]
    assert textbook.status == TextbookStatus.DRAFT
    assert metadata.textbook_id == textbook_id
    assert settings.textbook_id == textbook_id
    assert settings.is_public is True


def test_exec_failure_account_unauthorized(
    dummy_session,
    auth_failed_create_textbook_dependencies,
    create_textbook_dto,
):
    """Account認可に失敗した場合、教材の保存処理が実行されないこと。"""
    # Arrange
    usecase = CreateTextbookUsecase(session=dummy_session, dependencies=auth_failed_create_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(create_textbook_dto=create_textbook_dto)

    dependencies = auth_failed_create_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_id == create_textbook_dto.principal_id
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None
    assert dependencies.settings.input_textbook_settings is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_create_textbook_dependencies,
    create_textbook_dto,
):
    """Textbook保存で例外が発生した場合、例外が伝播し後続の保存が実行されないこと。"""
    # Arrange
    usecase = CreateTextbookUsecase(session=dummy_session, dependencies=save_failed_create_textbook_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(create_textbook_dto=create_textbook_dto)

    dependencies = save_failed_create_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook is not None
    assert dependencies.metadata.input_metadata is None
    assert dependencies.settings.input_textbook_settings is None
