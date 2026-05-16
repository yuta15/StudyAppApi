import pytest


@pytest.mark.parametrize(
    "is_public",
    [False, True],
)
def test_set_is_public_success_updates_is_public(textbook_settings, is_public):
    """公開状態をbool値に更新でき、教材IDは維持されること。"""
    # Arrange
    expected_textbook_id = textbook_settings.textbook_id

    # Act
    textbook_settings.set_is_public(is_public=is_public)

    # Assert
    assert textbook_settings.is_public is is_public
    assert textbook_settings.textbook_id == expected_textbook_id


@pytest.mark.parametrize(
    "is_public",
    [None, 1, "true"],
)
def test_set_is_public_failure_invalid_is_public_type(textbook_settings, is_public):
    """bool以外の公開状態では更新できず、状態が維持されること。"""
    # Arrange
    expected_textbook_id = textbook_settings.textbook_id
    expected_is_public = textbook_settings.is_public

    # Assert
    with pytest.raises(ValueError):
        textbook_settings.set_is_public(is_public=is_public)
    assert textbook_settings.textbook_id == expected_textbook_id
    assert textbook_settings.is_public is expected_is_public
