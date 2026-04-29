import pytest

from src.app.model.account.entities.subjects import AllowedIdentityProvider, Country
from src.app.model.account.entities.value_object import EmailStrings
from src.app.usecase.account.dto import (
    CreateAccountDTO,
    ModifyAccountDTO,
    ModifyBasicSettings,
    ModifyProfile,
)
from src.app.usecase.account.repository import (
    CreateAccountRepositories,
    DeleteAccountRepositories,
    ModifyAccountRepositories,
)
from src.test.usecase.account.repositories import (
    TestAccountAuthReadInterface,
    TestAccountRepositoryInterface,
    TestAccountMetadataInterface,
    TestAccountProfileInterface,
    TestAccountBasicSettingsInterface,
    TestAccountIdentityInterface,
)


@pytest.fixture
def positive_create_account_repositories(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return CreateAccountRepositories(
        account=TestAccountRepositoryInterface(return_account=account_generator()),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
        identity=TestAccountIdentityInterface(return_principal_identity=identity_generator()),
    )


@pytest.fixture
def account_negative_create_account_repositories(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return CreateAccountRepositories(
        account=TestAccountRepositoryInterface(return_account=account_generator(), is_negative=True),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
        identity=TestAccountIdentityInterface(return_principal_identity=identity_generator()),
    )


@pytest.fixture
def create_account_dto(account_name, display_name, email, identity_subject):
    return CreateAccountDTO(
        account_name=account_name,
        display_name=display_name,
        email=email,
        subject=identity_subject,
        provider=AllowedIdentityProvider.FIREBASE,
    )


@pytest.fixture
def modify_account_profile_dto(account_principal_id):
    return ModifyAccountDTO(
        principal_id=account_principal_id,
        profile=ModifyProfile(
            display_name="updated_display_name",
            email=EmailStrings("updated@example.com"),
            country=Country.JP,
        ),
        basic_settings=ModifyBasicSettings(),
    )


@pytest.fixture
def modify_account_basic_settings_dto(account_principal_id):
    return ModifyAccountDTO(
        principal_id=account_principal_id,
        profile=ModifyProfile(),
        basic_settings=ModifyBasicSettings(is_public=False),
    )


@pytest.fixture
def positive_delete_account_repositories(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return DeleteAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=True),
        account=TestAccountRepositoryInterface(return_account=account_generator()),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
        identity=TestAccountIdentityInterface(return_principal_identity=identity_generator()),
    )


@pytest.fixture
def negative_delete_account_repositories(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return DeleteAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=True),
        account=TestAccountRepositoryInterface(return_account=account_generator(), is_negative=True),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
        identity=TestAccountIdentityInterface(return_principal_identity=identity_generator()),
    )


@pytest.fixture
def auth_failed_delete_account_repositories(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
    identity_generator,
):
    return DeleteAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=False),
        account=TestAccountRepositoryInterface(return_account=account_generator(), is_negative=True),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
        identity=TestAccountIdentityInterface(return_principal_identity=identity_generator()),
    )


@pytest.fixture
def positive_modify_account_repository(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
):
    return ModifyAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=True),
        account=TestAccountRepositoryInterface(return_account=account_generator()),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
    )


@pytest.fixture
def auth_failed_modify_account_repository(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
):
    return ModifyAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=False),
        account=TestAccountRepositoryInterface(return_account=account_generator()),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
    )


@pytest.fixture
def get_failed_modify_account_repository(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
):
    return ModifyAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=True),
        account=TestAccountRepositoryInterface(return_account=account_generator(), is_negative=True),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator()),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
    )


@pytest.fixture
def save_failed_modify_account_repository(
    account_generator,
    metadata_generator,
    profile_generator,
    basic_settings_generator,
):
    return ModifyAccountRepositories(
        account_auth_read=TestAccountAuthReadInterface(auth_result=True),
        account=TestAccountRepositoryInterface(return_account=account_generator()),
        metadata=TestAccountMetadataInterface(return_account_metadata=metadata_generator(), is_negative=True),
        profile=TestAccountProfileInterface(return_account_profile=profile_generator()),
        basic_settings=TestAccountBasicSettingsInterface(return_account_basic_settings=basic_settings_generator()),
    )
