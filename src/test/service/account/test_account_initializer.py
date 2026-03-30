from uuid import UUID

from src.app.service.account.account_initializer import AccountInitializer
from src.app.model.account.principals.account import AccountStatus


def test_account_initialize(create_account_input, password_hasher_success, account_repository_success, hashed_password):
    initializer = AccountInitializer(
        password_hasher=password_hasher_success,
        account_repository=account_repository_success
    )
    account = initializer.initialize(create_account_input)
    assert isinstance(account.principal_id, UUID)
    assert account.display_name == create_account_input.display_name
    assert initializer.account_repository.account.principal_id == account.principal_id
    assert initializer.account_repository.account.display_name == create_account_input.display_name
    assert initializer.account_repository.account.status == AccountStatus.ACTIVE
    assert initializer.account_repository.account.metadata.created_at == initializer.account_repository.account.metadata.updated_at
    assert initializer.account_repository.profile.account_id == account.principal_id
    assert initializer.account_repository.profile.email == create_account_input.email
    assert initializer.account_repository.basic_settings.account_id == account.principal_id
    assert initializer.account_repository.auth_settings.account_id == account.principal_id
    assert initializer.account_repository.auth_settings.hashed_password == hashed_password