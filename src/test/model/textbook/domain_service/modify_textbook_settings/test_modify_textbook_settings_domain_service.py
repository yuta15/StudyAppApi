import pytest

from src.app.model.textbook import ModifyTextbookSettingsDomainService

INVALID_IS_PUBLIC_TYPE_IDS = ["integer", "string"]


def test_update_settings_success_updates_changed_is_public(textbook_settings, textbook_metadata):
    """公開状態に変更がある場合、設定とmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at
    expected_textbook_settings_id = textbook_settings.textbook_settings_id
    expected_textbook_id = textbook_settings.textbook_id

    # Act
    is_changed = ModifyTextbookSettingsDomainService.update_settings(
        settings=textbook_settings,
        metadata=textbook_metadata,
        is_public=False,
    )

    # Assert
    assert is_changed
    assert textbook_settings.is_public is False
    assert textbook_settings.textbook_settings_id == expected_textbook_settings_id
    assert textbook_settings.textbook_id == expected_textbook_id
    assert textbook_metadata.updated_at != updated_at


@pytest.mark.parametrize(
    "case",
    [
        "no_values",
        "same_is_public",
    ],
)
def test_update_settings_success_no_change(textbook_settings, textbook_metadata, case):
    """公開状態に実際の変更がない場合、設定とmetadataが更新されずFalseが返ること。"""
    # Arrange
    values = {
        "no_values": {},
        "same_is_public": {"is_public": textbook_settings.is_public},
    }[case]
    is_public = textbook_settings.is_public
    updated_at = textbook_metadata.updated_at
    expected_textbook_settings_id = textbook_settings.textbook_settings_id
    expected_textbook_id = textbook_settings.textbook_id

    # Act
    is_changed = ModifyTextbookSettingsDomainService.update_settings(
        settings=textbook_settings,
        metadata=textbook_metadata,
        **values,
    )

    # Assert
    assert not is_changed
    assert textbook_settings.is_public is is_public
    assert textbook_settings.textbook_settings_id == expected_textbook_settings_id
    assert textbook_settings.textbook_id == expected_textbook_id
    assert textbook_metadata.updated_at == updated_at


@pytest.mark.parametrize(
    "is_public",
    [1, "false"],
    ids=INVALID_IS_PUBLIC_TYPE_IDS,
)
def test_update_settings_failure_invalid_is_public_type(textbook_settings, textbook_metadata, is_public):
    """bool以外の公開状態では更新できず、設定とmetadataが維持されること。"""
    # Arrange
    current_is_public = textbook_settings.is_public
    updated_at = textbook_metadata.updated_at
    expected_textbook_settings_id = textbook_settings.textbook_settings_id
    expected_textbook_id = textbook_settings.textbook_id

    # Assert
    with pytest.raises(ValueError):
        ModifyTextbookSettingsDomainService.update_settings(
            settings=textbook_settings,
            metadata=textbook_metadata,
            is_public=is_public,
        )
    assert textbook_settings.is_public is current_is_public
    assert textbook_settings.textbook_settings_id == expected_textbook_settings_id
    assert textbook_settings.textbook_id == expected_textbook_id
    assert textbook_metadata.updated_at == updated_at
