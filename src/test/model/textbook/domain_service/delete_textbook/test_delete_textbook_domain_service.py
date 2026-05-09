from src.app.model.textbook import DeleteTextbookDomainService


def test_exec_success_deletes_textbook(textbook_data):
    """教材削除時にSettingsとMetadataが削除状態になること。"""
    # Arrange
    expected_textbook_settings_id = textbook_data.settings.textbook_settings_id
    expected_settings_textbook_id = textbook_data.settings.textbook_id
    expected_metadata_textbook_id = textbook_data.metadata.textbook_id

    # Act
    DeleteTextbookDomainService.exec(delete_textbook_data=textbook_data)

    # Assert
    assert not textbook_data.settings.is_public
    assert textbook_data.settings.textbook_settings_id == expected_textbook_settings_id
    assert textbook_data.settings.textbook_id == expected_settings_textbook_id
    assert textbook_data.metadata.textbook_id == expected_metadata_textbook_id
    assert textbook_data.metadata.deleted_at is not None
