import pytest

from src.app.core.exceptions import UnauthorizedError
from src.app.usecase.account.modify_account_settings_usecase import ModifyAccountSettingsUsecase
from src.test.usecase.account.repositories import TestException


def test_modify_account_settings_usecase_update_profile(
    dummy_session,
    positive_modify_account_repository,
    modify_account_profile_dto,
):
    """
    profileの値が更新できることをチェックする。
    """
    principal_id = modify_account_profile_dto.principal_id
    profile_dto = modify_account_profile_dto.profile

    usecase = ModifyAccountSettingsUsecase(session=dummy_session, repositories=positive_modify_account_repository)
    result = usecase.exec(modify_account_dto=modify_account_profile_dto)

    account_auth_read = positive_modify_account_repository.account_auth_read
    account = positive_modify_account_repository.account
    metadata = positive_modify_account_repository.metadata
    profile = positive_modify_account_repository.profile
    basic_settings = positive_modify_account_repository.basic_settings

    assert dummy_session.is_called
    assert account_auth_read.input_principal_id == principal_id
    assert account.input_principal_id == principal_id
    assert metadata.input_principal_id == principal_id
    assert profile.input_principal_id == principal_id
    assert basic_settings.input_principal_id == principal_id

    assert profile.input_profile.principal_id == principal_id
    assert profile.input_profile.display_name == profile_dto.display_name
    assert profile.input_profile.email == profile_dto.email
    assert profile.input_profile.country == profile_dto.country
    assert metadata.input_metadata.principal_id == principal_id
    assert metadata.input_metadata.updated_at != metadata.input_metadata.created_at
    assert basic_settings.input_basic_settings == None

    assert result.principal_id == principal_id
    assert result.profile.display_name == profile_dto.display_name
    assert result.profile.email == profile_dto.email
    assert result.profile.country == profile_dto.country


def test_modify_account_settings_usecase_update_basic_settings(
    dummy_session,
    positive_modify_account_repository,
    modify_account_basic_settings_dto,
):
    """
    basic_settingsの値が更新できることをチェックする。
    """
    principal_id = modify_account_basic_settings_dto.principal_id
    basic_settings_dto = modify_account_basic_settings_dto.basic_settings

    usecase = ModifyAccountSettingsUsecase(session=dummy_session, repositories=positive_modify_account_repository)
    result = usecase.exec(modify_account_dto=modify_account_basic_settings_dto)

    account_auth_read = positive_modify_account_repository.account_auth_read
    account = positive_modify_account_repository.account
    metadata = positive_modify_account_repository.metadata
    profile = positive_modify_account_repository.profile
    basic_settings = positive_modify_account_repository.basic_settings

    assert dummy_session.is_called
    assert account_auth_read.input_principal_id == principal_id
    assert account.input_principal_id == principal_id
    assert metadata.input_principal_id == principal_id
    assert profile.input_principal_id == principal_id
    assert basic_settings.input_principal_id == principal_id

    assert basic_settings.input_basic_settings.principal_id == principal_id
    assert basic_settings.input_basic_settings.is_public == basic_settings_dto.is_public
    assert metadata.input_metadata.principal_id == principal_id
    assert metadata.input_metadata.updated_at != metadata.input_metadata.created_at
    assert profile.input_profile == None

    assert result.principal_id == principal_id
    assert result.settings.is_public == basic_settings_dto.is_public


def test_modify_account_settings_usecase_auth_raises(
    dummy_session,
    auth_failed_modify_account_repository,
    modify_account_profile_dto,
):
    """
    認可エラーが発生した場合にエラーが伝搬すること。
    """
    usecase = ModifyAccountSettingsUsecase(session=dummy_session, repositories=auth_failed_modify_account_repository)

    with pytest.raises(UnauthorizedError):
        usecase.exec(modify_account_dto=modify_account_profile_dto)


def test_modify_account_settings_usecase_get_raises(
    dummy_session,
    get_failed_modify_account_repository,
    modify_account_profile_dto,
):
    """
    getにてエラーが発生した場合にエラーが伝搬すること。
    """
    usecase = ModifyAccountSettingsUsecase(session=dummy_session, repositories=get_failed_modify_account_repository)

    with pytest.raises(TestException):
        usecase.exec(modify_account_dto=modify_account_profile_dto)


def test_modify_account_settings_usecase_save_raises(
    dummy_session,
    save_failed_modify_account_repository,
    modify_account_profile_dto,
):
    """
    saveにてエラーが発生した場合にエラーが伝搬すること。
    """
    usecase = ModifyAccountSettingsUsecase(session=dummy_session, repositories=save_failed_modify_account_repository)

    with pytest.raises(TestException):
        usecase.exec(modify_account_dto=modify_account_profile_dto)
