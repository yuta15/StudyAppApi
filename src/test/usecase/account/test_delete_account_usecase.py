from datetime import datetime

import pytest

from src.app.model.account.entities.principals import AccountStatus
from src.app.usecase.account.delete_account_usecase import DeleteAccountUsecase
from src.app.core.exceptions import UnauthorizedError


def test_delete_account_usecase_success(
        dummy_session,
        positive_delete_account_repositories,
        account_principal_id,
        account_generator,
        profile_generator,
        basic_settings_generator,
        metadata_generator,
        identity_generator
    ):
    usecase = DeleteAccountUsecase(session=dummy_session, repositories=positive_delete_account_repositories)
    usecase.exec(principal_id=account_principal_id)

    account = account_generator()
    profile = profile_generator()
    basic_settings = basic_settings_generator()
    metadata = metadata_generator()
    identity = identity_generator()

    account.to_delete()
    profile.delete()
    basic_settings.delete()
    metadata.delete()
    identity.delete()

    input_account = positive_delete_account_repositories.account
    input_metadata = positive_delete_account_repositories.metadata
    input_profile = positive_delete_account_repositories.profile
    input_basic_settings = positive_delete_account_repositories.basic_settings
    input_identity = positive_delete_account_repositories.identity

    # GETする時の引数が正しいか
    assert input_account.input_principal_id == account_principal_id
    assert input_metadata.input_principal_id == account_principal_id
    assert input_profile.input_principal_id == account_principal_id
    assert input_basic_settings.input_principal_id == account_principal_id
    assert input_identity.input_principal_id == account_principal_id

    # SAVEする時の引数が正しいか
    assert input_account.input_account.principal_id == account.principal_id
    assert input_account.input_account.account_name == account.account_name
    assert input_account.input_account.status == AccountStatus.DELETED
    assert input_metadata.input_metadata.principal_id == metadata.principal_id
    assert input_metadata.input_metadata.metadata_id == metadata.metadata_id
    assert isinstance(input_metadata.input_metadata.deleted_at, datetime)
    assert input_profile.input_profile.principal_id == profile.principal_id
    assert input_profile.input_profile.display_name == profile.display_name
    assert input_profile.input_profile.email == profile.email
    assert input_basic_settings.input_basic_settings.principal_id == profile.principal_id
    assert input_basic_settings.input_basic_settings.is_public == basic_settings.is_public
    assert input_identity.input_identity.principal_id == identity.principal_id
    assert input_identity.input_identity.subject == identity.subject


def test_delete_account_usecase_failure(dummy_session, negative_delete_account_repositories, account_principal_id):
    usecase = DeleteAccountUsecase(session=dummy_session, repositories=negative_delete_account_repositories)
    with pytest.raises(Exception):
        usecase.exec(principal_id=account_principal_id)


def test_delete_account_usecase_auth_failure(
        dummy_session,
        auth_failed_delete_account_repositories,
        account_principal_id
    ):
    usecase = DeleteAccountUsecase(session=dummy_session, repositories=auth_failed_delete_account_repositories)
    with pytest.raises(UnauthorizedError):
        usecase.exec(principal_id=account_principal_id)
