import pytest

from src.app.model.account import CreateAccountInput


@pytest.fixture
def create_account_input(account_name, display_name, email, identity_provider, identity_subject):
    return CreateAccountInput(
        account_name=account_name,
        display_name=display_name,
        email=email,
        subject=identity_subject,
        provider=identity_provider,
    )
