import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.service.authorization_service.textbook import TextbookAuthService
from src.test.service.dummy_textbook_auth_dependencies import DummyAccountAuthService, DummyTextbookAuthReader


def test_auth_success_authorized_author(account_principal_id, textbook_id):
    """認可済みAccountかつTextbook著者の場合は認可できること。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(result=True)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Act
    result = service.auth(principal_id=account_principal_id, textbook_id=textbook_id)

    # Assert
    assert result is None
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_textbook_id == textbook_id


def test_auth_failure_account_unauthorized(account_principal_id, textbook_id):
    """Account認可に失敗した場合は認可できないこと。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=False)
    textbook_auth_reader = DummyTextbookAuthReader(result=True)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Assert
    with pytest.raises(UnauthorizedError):
        service.auth(
            principal_id=account_principal_id,
            textbook_id=textbook_id,
        )
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id is None
    assert textbook_auth_reader._input_textbook_id is None


def test_auth_failure_principal_is_not_textbook_author(
    account_principal_id,
    textbook_id,
):
    """Textbook著者ではない場合は認可できず、例外メッセージにtextbook_idを含むこと。"""
    # Arrange
    account_auth_service = DummyAccountAuthService(is_authorized=True)
    textbook_auth_reader = DummyTextbookAuthReader(result=False)
    service = TextbookAuthService(account_auth_service=account_auth_service, repository=textbook_auth_reader)

    # Assert
    with pytest.raises(UnauthorizedError) as error:
        service.auth(principal_id=account_principal_id, textbook_id=textbook_id)
    assert str(textbook_id) in str(error.value)
    assert account_auth_service._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_principal_id == account_principal_id
    assert textbook_auth_reader._input_textbook_id == textbook_id
