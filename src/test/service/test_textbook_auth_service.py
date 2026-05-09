import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.model.textbook import TextbookStatus
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.test.service.dummy_textbook_auth_dependencies import DummyAccountAuthService, DummyTextbookAuthReader


def test_auth_create_success_authorized_account(account_principal_id):
    """認可済みAccountの場合、教材作成を認可できること。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(result=False)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Act
    result = service.auth_create(principal_id=account_principal_id)

    # Assert
    assert result is None
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id is None
    assert textbook_auth_reader._input_visibility_textbook_id is None


def test_auth_create_failure_account_unauthorized(account_principal_id):
    """Account認可に失敗した場合、教材作成を認可できないこと。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=False)
    textbook_auth_reader = DummyTextbookAuthReader(result=False)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Assert
    with pytest.raises(UnauthorizedError):
        service.auth_create(principal_id=account_principal_id)
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id is None
    assert textbook_auth_reader._input_visibility_textbook_id is None


def test_auth_manage_success_authorized_author(account_principal_id, textbook_id):
    """認可済みAccountかつTextbook著者の場合、管理操作を認可できること。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(result=True)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Act
    result = service.auth_manage(principal_id=account_principal_id, textbook_id=textbook_id)

    # Assert
    assert result is None
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_textbook_id == textbook_id
    assert textbook_auth_reader._input_visibility_textbook_id is None


def test_auth_manage_failure_account_unauthorized(account_principal_id, textbook_id):
    """Account認可に失敗した場合、管理操作を認可できないこと。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=False)
    textbook_auth_reader = DummyTextbookAuthReader(result=True)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Assert
    with pytest.raises(UnauthorizedError):
        service.auth_manage(principal_id=account_principal_id, textbook_id=textbook_id)
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id is None
    assert textbook_auth_reader._input_textbook_id is None


def test_auth_manage_failure_principal_is_not_textbook_author(
    account_principal_id,
    textbook_id,
):
    """Textbook著者ではない場合、管理操作を認可できないこと。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(result=False)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Assert
    with pytest.raises(UnauthorizedError) as error:
        service.auth_manage(principal_id=account_principal_id, textbook_id=textbook_id)
    assert str(textbook_id) in str(error.value)
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_textbook_id == textbook_id


def test_auth_read_success_publicly_readable_textbook(account_principal_id, textbook_id):
    """公開済み教材の場合、Account認可と著者認可なしで閲覧を認可できること。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=False)
    textbook_auth_reader = DummyTextbookAuthReader(
        result=False,
        is_public=True,
        status=TextbookStatus.PUBLISHED,
    )
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Act
    result = service.auth_read(principal_id=account_principal_id, textbook_id=textbook_id)

    # Assert
    assert result is None
    assert textbook_auth_reader._input_visibility_textbook_id == textbook_id
    assert account_auth_service._input_principal_id is None
    assert textbook_auth_reader._input_principal_id is None
    assert textbook_auth_reader._input_textbook_id is None


def test_auth_read_success_private_textbook_author(account_principal_id, textbook_id):
    """非公開閲覧状態の教材でも、認可済み著者なら閲覧を認可できること。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(
        result=True,
        is_public=False,
        status=TextbookStatus.DRAFT,
    )
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Act
    result = service.auth_read(principal_id=account_principal_id, textbook_id=textbook_id)

    # Assert
    assert result is None
    assert textbook_auth_reader._input_visibility_textbook_id == textbook_id
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_textbook_id == textbook_id


def test_auth_read_failure_private_textbook_without_principal(textbook_id):
    """非公開閲覧状態の教材でprincipal_idがない場合、閲覧を認可できないこと。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(
        result=True,
        is_public=False,
        status=TextbookStatus.DRAFT,
    )
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Assert
    with pytest.raises(UnauthorizedError):
        service.auth_read(principal_id=None, textbook_id=textbook_id)
    assert textbook_auth_reader._input_visibility_textbook_id == textbook_id
    assert account_auth_service._input_principal_id is None
    assert textbook_auth_reader._input_principal_id is None
