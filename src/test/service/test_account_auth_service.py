# 認可対象を渡して想定通りの認可結果になること。
from src.app.service.authorization_service.account_auth_service import AccountAuthService


def test_account_auth_service_profile_success(success_account_repo, profile_account_auth_input):
    service = AccountAuthService(success_account_repo)
    assert service.is_allowed(profile_account_auth_input) == True
    assert success_account_repo._called_args["account_id"] == profile_account_auth_input.principal_id
    assert success_account_repo._called_args["subject_type"] == profile_account_auth_input.subject_type

def test_account_auth_service_basic_settings_success(success_account_repo, basic_settings_account_auth_input):
    service = AccountAuthService(success_account_repo)
    assert service.is_allowed(basic_settings_account_auth_input) == True
    assert success_account_repo._called_args["account_id"] == basic_settings_account_auth_input.principal_id
    assert success_account_repo._called_args["subject_type"] == basic_settings_account_auth_input.subject_type


def test_account_auth_service_profile_failure(failed_account_repo, profile_account_auth_input):
    service = AccountAuthService(failed_account_repo)
    assert service.is_allowed(profile_account_auth_input) == False
    assert failed_account_repo._called_args["account_id"] == profile_account_auth_input.principal_id
    assert failed_account_repo._called_args["subject_type"] == profile_account_auth_input.subject_type

def test_account_auth_service_basic_settings_failure(failed_account_repo, basic_settings_account_auth_input):
    service = AccountAuthService(failed_account_repo)
    assert service.is_allowed(basic_settings_account_auth_input) == False
    assert failed_account_repo._called_args["account_id"] == basic_settings_account_auth_input.principal_id
    assert failed_account_repo._called_args["subject_type"] == basic_settings_account_auth_input.subject_type
