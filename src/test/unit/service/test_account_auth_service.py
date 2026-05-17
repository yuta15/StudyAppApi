import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.service.authorization_service.account import AccountAuthService


def test_found_account_auth_service(found_account_auth_reader, account_principal_id):
    service = AccountAuthService(found_account_auth_reader)
    service.auth(principal_id=account_principal_id)
    assert found_account_auth_reader._input_principal_id == account_principal_id


def test_not_found_account_auth_service(not_found_account_auth_reader, account_principal_id):
    service = AccountAuthService(not_found_account_auth_reader)
    with pytest.raises(UnauthorizedError):
        service.auth(principal_id=account_principal_id)


def test_account_auth_service_failed(negative_account_auth_reader, account_principal_id):
    service = AccountAuthService(negative_account_auth_reader)
    with pytest.raises(Exception):
        service.auth(principal_id=account_principal_id)
