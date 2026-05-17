from datetime import datetime, timezone

import pytest
from sqlmodel import select

from src.app.infra.account import (
    AccountBasicSettingsRepository,
    AccountIdentityRepository,
    AccountMetadataRepository,
    AccountProfileRepository,
)
from src.app.model.account import (
    AccountBasicSettings,
    AccountIdentity,
    AccountMetadata,
    AccountProfile,
    Country,
    EmailStrings,
)
from src.app.schemas.db.account import (
    AccountBasicSettingsTable,
    AccountIdentityTable,
    AccountMetadataTable,
    AccountProfileTable,
)

pytestmark = pytest.mark.integration


def test_save_success_updates_profile(
    infra_session,
    persisted_account_table,
    account_principal_id,
    display_name,
    email,
):
    """既存Profile保存時に変更可能な値を更新できること。"""
    # Arrange
    infra_session.add(
        AccountProfileTable(
            principal_id=account_principal_id,
            display_name=display_name,
            email=email.value,
            country=Country.NOT_SET,
        )
    )
    infra_session.flush()
    repository = AccountProfileRepository(session=infra_session)
    profile = AccountProfile(
        principal_id=account_principal_id,
        display_name="updated_display_name",
        email=EmailStrings("updated_email@example.com"),
        country=Country.JP,
    )

    # Act
    repository.save(profile=profile)
    infra_session.flush()
    saved_profile = repository.get(principal_id=account_principal_id)

    # Assert
    assert saved_profile == profile


def test_get_success_returns_basic_settings(
    infra_session,
    persisted_account_table,
    account_principal_id,
):
    """DB値からAccountBasicSettingsを復元できること。"""
    # Arrange
    infra_session.add(AccountBasicSettingsTable(principal_id=account_principal_id, is_public=False))
    infra_session.flush()
    repository = AccountBasicSettingsRepository(session=infra_session)

    # Act
    basic_settings = repository.get(principal_id=account_principal_id)

    # Assert
    assert basic_settings == AccountBasicSettings(principal_id=account_principal_id, is_public=False)


def test_get_success_returns_metadata(
    infra_session,
    persisted_account_table,
    account_principal_id,
):
    """DB値からAccountMetadataを復元できること。"""
    # Arrange
    created_at = datetime(2026, 5, 1, tzinfo=timezone.utc)
    updated_at = datetime(2026, 5, 2, tzinfo=timezone.utc)
    infra_session.add(
        AccountMetadataTable(
            principal_id=account_principal_id,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=None,
        )
    )
    infra_session.flush()
    repository = AccountMetadataRepository(session=infra_session)

    # Act
    metadata = repository.get(principal_id=account_principal_id)

    # Assert
    assert metadata == AccountMetadata(
        principal_id=account_principal_id,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=None,
    )


def test_get_success_returns_identity(
    infra_session,
    persisted_account_table,
    account_principal_id,
    identity_provider,
    identity_subject,
):
    """DB値からAccountIdentityを復元できること。"""
    # Arrange
    infra_session.add(
        AccountIdentityTable(
            principal_id=account_principal_id,
            provider=identity_provider,
            subject=identity_subject,
        )
    )
    infra_session.flush()
    repository = AccountIdentityRepository(session=infra_session)

    # Act
    identity = repository.get(principal_id=account_principal_id)

    # Assert
    assert identity == AccountIdentity(
        principal_id=account_principal_id,
        provider=identity_provider,
        subject=identity_subject,
    )


def test_delete_success_removes_identity(
    infra_session,
    persisted_account_table,
    account_principal_id,
    identity_provider,
    identity_subject,
):
    """Identity削除時に対象行を削除できること。"""
    # Arrange
    identity_table = AccountIdentityTable(
        principal_id=account_principal_id,
        provider=identity_provider,
        subject=identity_subject,
    )
    infra_session.add(identity_table)
    infra_session.flush()
    repository = AccountIdentityRepository(session=infra_session)

    # Act
    repository.delete(principal_id=account_principal_id)
    infra_session.flush()

    # Assert
    identity_table = infra_session.exec(
        select(AccountIdentityTable).where(AccountIdentityTable.principal_id == account_principal_id)
    ).one_or_none()
    assert identity_table is None
