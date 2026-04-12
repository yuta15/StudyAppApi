import pytest

from src.app.model.account.service.create_account_domain_service import CreateAccountDomainService


def test_success(account_name, display_name, email):
    result = CreateAccountDomainService.exec(
        account_name=account_name,
        display_name=display_name,
        email=email,
    )
    assert result.account.account_name == account_name
    assert result.profile.display_name == display_name
    assert result.profile.email == email
    assert result.account.principal_id == result.profile.principal_id
    assert result.account.principal_id == result.metadata.principal_id
    assert result.account.principal_id == result.basic_settings.principal_id


def test_ignore_account_name_failure(display_name, email):
    with pytest.raises(Exception):
        CreateAccountDomainService.exec(
            account_name=None,
            display_name=display_name,
            email=email,
        )

def test_ignore_display_name_failure(account_name, email):
    with pytest.raises(Exception):
        CreateAccountDomainService.exec(
            account_name=account_name,
            display_name=None,
            email=email,
        )

def test_ignore_email_failure(account_name, display_name):
    with pytest.raises(Exception):
        CreateAccountDomainService.exec(
            account_name=account_name,
            display_name=display_name,
            email=None,
        )