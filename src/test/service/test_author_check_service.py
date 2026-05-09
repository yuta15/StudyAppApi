import pytest

from src.app.core.exceptions import NotFoundError
from src.app.service.author_check_service import AuthorCheckService
from src.app.service.interface.account import AccountAuthReadInterface


class AuthorCheckServiceTestException(Exception):
    """AuthorCheckServiceテスト用のダミーエラー"""


class DummyAccountAuthRead(AccountAuthReadInterface):
    def __init__(self, result: bool, is_negative: bool = False):
        self.result = result
        self.is_negative = is_negative
        self.input_principal_id = None

    def has_specified_active_user(self, principal_id):
        self.input_principal_id = principal_id
        if self.is_negative:
            raise AuthorCheckServiceTestException()
        return self.result


def test_check_active_success_active_author(account_principal_id):
    """追加対象アカウントが有効な場合、例外が発生しないこと。"""
    # Arrange
    repository = DummyAccountAuthRead(result=True)
    service = AuthorCheckService(repository=repository)

    # Act
    service.check_active(author_id=account_principal_id)

    # Assert
    assert repository.input_principal_id == account_principal_id


def test_check_active_failure_inactive_author(account_principal_id):
    """追加対象アカウントが有効でない場合、NotFoundErrorになること。"""
    # Arrange
    repository = DummyAccountAuthRead(result=False)
    service = AuthorCheckService(repository=repository)

    # Assert
    with pytest.raises(NotFoundError):
        service.check_active(author_id=account_principal_id)

    assert repository.input_principal_id == account_principal_id


def test_check_active_failure_repository_error(account_principal_id):
    """Repositoryで例外が発生した場合、例外が伝播すること。"""
    # Arrange
    repository = DummyAccountAuthRead(result=True, is_negative=True)
    service = AuthorCheckService(repository=repository)

    # Assert
    with pytest.raises(AuthorCheckServiceTestException):
        service.check_active(author_id=account_principal_id)

    assert repository.input_principal_id == account_principal_id
