import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.usecase.account.dto import AccountOutputDTO
from src.app.usecase.account.get_account_usecase import GetAccountUsecase
from src.test.unit.usecase.account.repositories import TestException


def test_exec_success_returns_account_output(
    dummy_session,
    positive_get_account_repositories,
    account_principal_id,
):
    """認可済みアカウントの情報をAccountOutputDTOとして返せること。"""
    # Arrange
    usecase = GetAccountUsecase(session=dummy_session, repositories=positive_get_account_repositories)

    # Act
    result = usecase.exec(principal_id=account_principal_id)

    # Assert
    account_auth_read = positive_get_account_repositories.account_auth_read
    account = positive_get_account_repositories.account
    metadata = positive_get_account_repositories.metadata
    profile = positive_get_account_repositories.profile
    basic_settings = positive_get_account_repositories.basic_settings

    assert dummy_session.is_called
    assert account_auth_read.input_principal_id == account_principal_id
    assert account.input_principal_id == account_principal_id
    assert metadata.input_principal_id == account_principal_id
    assert profile.input_principal_id == account_principal_id
    assert basic_settings.input_principal_id == account_principal_id

    assert isinstance(result, AccountOutputDTO)
    assert result.principal_id == account_principal_id
    assert result.account_name == account.return_account.account_name
    assert result.status == account.return_account.status
    assert result.metadata.created_at == metadata.return_account_metadata.created_at
    assert result.metadata.last_update == metadata.return_account_metadata.updated_at
    assert result.profile.display_name == profile.return_account_profile.display_name
    assert result.profile.email == profile.return_account_profile.email
    assert result.profile.country == profile.return_account_profile.country
    assert result.settings.is_public == basic_settings.return_account_basic_settings.is_public


def test_exec_failure_unauthorized(
    dummy_session,
    auth_failed_get_account_repositories,
    account_principal_id,
):
    """非アクティブなアカウントでは認可エラーになること。"""
    # Arrange
    usecase = GetAccountUsecase(session=dummy_session, repositories=auth_failed_get_account_repositories)

    # Assert
    with pytest.raises(UnauthorizedError):
        usecase.exec(principal_id=account_principal_id)


def test_exec_failure_get_error(
    dummy_session,
    get_failed_get_account_repositories,
    account_principal_id,
):
    """取得処理で発生した例外が伝搬すること。"""
    # Arrange
    usecase = GetAccountUsecase(session=dummy_session, repositories=get_failed_get_account_repositories)

    # Assert
    with pytest.raises(TestException):
        usecase.exec(principal_id=account_principal_id)
