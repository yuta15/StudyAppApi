from fastapi import Depends
from sqlmodel import Session

from src.app.endpoints.deps.db import get_session
from src.app.infra.account import (
    AccountBasicSettingsRepository,
    AccountIdentityRepository,
    AccountMetadataRepository,
    AccountProfileRepository,
    AccountRepository,
)
from src.app.infra.auth import AccountAuthReadRepository
from src.app.usecase.account.repository import (
    CreateAccountRepositories,
    DeleteAccountRepositories,
    GetAccountRepositories,
    ModifyAccountRepositories,
)


def get_create_account_repositories(session: Session = Depends(get_session)) -> CreateAccountRepositories:
    return CreateAccountRepositories(
        account=AccountRepository(session=session),
        metadata=AccountMetadataRepository(session=session),
        profile=AccountProfileRepository(session=session),
        basic_settings=AccountBasicSettingsRepository(session=session),
        identity=AccountIdentityRepository(session=session),
    )


def get_get_account_repositories(session: Session = Depends(get_session)) -> GetAccountRepositories:
    return GetAccountRepositories(
        account_auth_read=AccountAuthReadRepository(session=session),
        account=AccountRepository(session=session),
        metadata=AccountMetadataRepository(session=session),
        profile=AccountProfileRepository(session=session),
        basic_settings=AccountBasicSettingsRepository(session=session),
    )


def get_modify_account_repositories(session: Session = Depends(get_session)) -> ModifyAccountRepositories:
    return ModifyAccountRepositories(
        account_auth_read=AccountAuthReadRepository(session=session),
        account=AccountRepository(session=session),
        metadata=AccountMetadataRepository(session=session),
        profile=AccountProfileRepository(session=session),
        basic_settings=AccountBasicSettingsRepository(session=session),
    )


def get_delete_account_repositories(session: Session = Depends(get_session)) -> DeleteAccountRepositories:
    return DeleteAccountRepositories(
        account_auth_read=AccountAuthReadRepository(session=session),
        account=AccountRepository(session=session),
        metadata=AccountMetadataRepository(session=session),
        profile=AccountProfileRepository(session=session),
        basic_settings=AccountBasicSettingsRepository(session=session),
        identity=AccountIdentityRepository(session=session),
    )
