import pytest

from src.app.model.account.service.create_account_domain_service import CreateAccountDomainService


def test_success(create_account_input):
    account_name = create_account_input.account_name
    display_name = create_account_input.display_name
    email = create_account_input.email
    provider = create_account_input.provider
    subject = create_account_input.subject

    result = CreateAccountDomainService.exec(create_account_input)
    assert result.account.account_name == account_name
    assert result.profile.display_name == display_name
    assert result.profile.email == email
    assert result.identity.provider == provider
    assert result.identity.subject == subject

    assert result.account.principal_id == result.profile.principal_id
    assert result.account.principal_id == result.metadata.principal_id
    assert result.account.principal_id == result.basic_settings.principal_id
    assert result.account.principal_id == result.identity.principal_id