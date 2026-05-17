import pytest

from src.app.model.textbook import TextbookSettings

INVALID_UUID_IDS = ["none", "integer", "string"]


def test_new_success_creates_textbook_settings(textbook_id):
    """新規作成時に教材ID、公開状態の初期値が設定されること。"""
    # Act
    settings = TextbookSettings.new(textbook_id=textbook_id)

    # Assert
    assert settings.textbook_id == textbook_id
    assert settings.is_public is True


@pytest.mark.parametrize(
    "textbook_id",
    [None, 1, "not-uuid"],
    ids=INVALID_UUID_IDS,
)
def test_new_failure_invalid_textbook_id(textbook_id):
    """不正な教材IDでは作成できないこと。"""
    # Assert
    with pytest.raises(ValueError):
        TextbookSettings.new(textbook_id=textbook_id)
