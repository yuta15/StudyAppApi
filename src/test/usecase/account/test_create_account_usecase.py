import pytest
from uuid import UUID

from src.app.usecase.account.create_account_usecase import CreateAccountUsecase
from src.test.usecase.account.repositories import TestException


def test_usecase(dummy_session, positive_create_account_repositories, create_account_dto):
    usecase = CreateAccountUsecase(session=dummy_session, repositories=positive_create_account_repositories)
    principal_id = usecase.exec(create_account_dto=create_account_dto)

    account = positive_create_account_repositories.account.input_account
    metadata = positive_create_account_repositories.metadata.input_metadata
    profile = positive_create_account_repositories.profile.input_profile
    basic_settings = positive_create_account_repositories.basic_settings.input_basic_settings
    identity = positive_create_account_repositories.identity.input_identity

    assert isinstance(principal_id, UUID)
    assert dummy_session.is_called
    assert account.principal_id == principal_id
    assert account.account_name == create_account_dto.account_name
    assert metadata.principal_id == principal_id
    assert profile.principal_id == principal_id
    assert profile.display_name == create_account_dto.display_name
    assert profile.email == create_account_dto.email
    assert basic_settings.principal_id == principal_id
    assert identity.principal_id == principal_id
    assert identity.subject == create_account_dto.subject
    assert identity.provider == create_account_dto.provider


def test_usecase_raise_save(dummy_session, account_negative_create_account_repositories, create_account_dto):
    with pytest.raises(TestException):
        usecase = CreateAccountUsecase(
            session=dummy_session,
            repositories=account_negative_create_account_repositories,
        )
        usecase.exec(create_account_dto=create_account_dto)
