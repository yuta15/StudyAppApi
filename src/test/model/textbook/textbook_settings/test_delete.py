def test_delete_success_makes_textbook_settings_private(textbook_settings):
    """削除時に設定が非公開になり、教材IDは維持されること。"""
    # Arrange
    textbook_settings.set_is_public(is_public=True)
    expected_textbook_id = textbook_settings.textbook_id

    # Act
    textbook_settings.delete()

    # Assert
    assert textbook_settings.is_public is False
    assert textbook_settings.textbook_id == expected_textbook_id


def test_delete_success_keeps_private_textbook_settings_private(textbook_settings):
    """非公開の設定も削除でき、非公開のまま維持されること。"""
    # Arrange
    textbook_settings.set_is_public(is_public=False)
    expected_textbook_id = textbook_settings.textbook_id

    # Act
    textbook_settings.delete()

    # Assert
    assert textbook_settings.is_public is False
    assert textbook_settings.textbook_id == expected_textbook_id
