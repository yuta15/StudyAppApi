import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.model.textbook import TextbookStatus
from src.app.usecase.textbook.dto import OutputTextbookModified
from src.app.usecase.textbook.modify_textbook_usecase import ModifyTextbookUsecase
from src.test.unit.usecase.textbook.repositories import TextbookUsecaseTestException


def test_exec_success_updates_textbook(dummy_session, positive_modify_textbook_dependencies, modify_textbook_dto):
    """認可済み著者が教材本体を変更するとTextbookとMetadataが保存され、変更後のOutputが返ること。"""
    # Arrange
    usecase = ModifyTextbookUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Act
    result = usecase.exec(modify_textbook_dto=modify_textbook_dto)

    # Assert
    dependencies = positive_modify_textbook_dependencies
    textbook = dependencies.textbook.input_textbook
    metadata = dependencies.metadata.input_metadata

    assert isinstance(result, OutputTextbookModified)
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_id == modify_textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_principal_id == modify_textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == modify_textbook_dto.textbook_id
    assert dependencies.textbook.input_textbook_id == modify_textbook_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == modify_textbook_dto.textbook_id
    assert textbook.status == TextbookStatus.PUBLISHED
    assert metadata.updated_at != metadata.created_at
    assert result.textbook_id == modify_textbook_dto.textbook_id
    assert result.title == textbook.title
    assert result.status == TextbookStatus.PUBLISHED
    assert result.metadata.created_at == metadata.created_at
    assert result.metadata.updated_at == metadata.updated_at


def test_exec_success_no_change_skips_save(
    dummy_session,
    positive_modify_textbook_dependencies,
    no_change_modify_textbook_dto,
):
    """教材本体に変更がない場合、TextbookとMetadataが保存されず現在値のOutputが返ること。"""
    # Arrange
    usecase = ModifyTextbookUsecase(session=dummy_session, dependencies=positive_modify_textbook_dependencies)

    # Act
    result = usecase.exec(modify_textbook_dto=no_change_modify_textbook_dto)

    # Assert
    dependencies = positive_modify_textbook_dependencies
    textbook = dependencies.textbook.return_textbook
    metadata = dependencies.metadata.return_metadata

    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook_id == no_change_modify_textbook_dto.textbook_id
    assert dependencies.metadata.input_textbook_id == no_change_modify_textbook_dto.textbook_id
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None
    assert textbook.status == TextbookStatus.DRAFT
    assert metadata.updated_at == metadata.created_at
    assert result.textbook_id == no_change_modify_textbook_dto.textbook_id
    assert result.title == textbook.title
    assert result.status == TextbookStatus.DRAFT
    assert result.metadata.created_at == metadata.created_at
    assert result.metadata.updated_at == metadata.updated_at


def test_exec_failure_textbook_unauthorized(
    dummy_session,
    auth_failed_modify_textbook_dependencies,
    modify_textbook_dto,
):
    """Textbook著者認可に失敗した場合、変更対象の取得と保存が実行されないこと。"""
    # Arrange
    usecase = ModifyTextbookUsecase(session=dummy_session, dependencies=auth_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(modify_textbook_dto=modify_textbook_dto)

    dependencies = auth_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.account_auth_read.input_principal_id == modify_textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_principal_id == modify_textbook_dto.principal_id
    assert dependencies.textbook_auth_read.input_textbook_id == modify_textbook_dto.textbook_id
    assert dependencies.textbook.input_textbook_id is None
    assert dependencies.metadata.input_textbook_id is None
    assert dependencies.textbook.input_textbook is None
    assert dependencies.metadata.input_metadata is None


def test_exec_failure_save_error_propagates(
    dummy_session,
    save_failed_modify_textbook_dependencies,
    modify_textbook_dto,
):
    """Textbook保存で例外が発生した場合、例外が伝播しMetadata保存が実行されないこと。"""
    # Arrange
    usecase = ModifyTextbookUsecase(session=dummy_session, dependencies=save_failed_modify_textbook_dependencies)

    # Assert
    with pytest.raises(TextbookUsecaseTestException):
        usecase.exec(modify_textbook_dto=modify_textbook_dto)

    dependencies = save_failed_modify_textbook_dependencies
    assert dummy_session.is_called
    assert dependencies.textbook.input_textbook is not None
    assert dependencies.metadata.input_metadata is None
