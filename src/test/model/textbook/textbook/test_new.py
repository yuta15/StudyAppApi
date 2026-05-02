from uuid import UUID

import pytest

from src.app.model.textbook import Textbook

INVALID_TITLE_TYPE_IDS = ["none", "integer", "string"]
INVALID_UUID_IDS = ["none", "integer", "string"]


def test_new_success_creates_textbook(textbook_title, account_principal_id):
    """新規作成時にID、タイトル、著者、空の章リストが設定されること。"""
    # Act
    textbook = Textbook.new(title=textbook_title, author_id=account_principal_id)

    # Assert
    assert isinstance(textbook.textbook_id, UUID)
    assert textbook.title == textbook_title
    assert textbook.author_ids == [account_principal_id]
    assert textbook.chapter_ids == []
    assert textbook.is_public is True


@pytest.mark.parametrize(
    "title",
    [None, 1, "Python"],
    ids=INVALID_TITLE_TYPE_IDS,
)
def test_new_failure_invalid_title_type(title, account_principal_id):
    """TitleString以外のタイトルでは作成できないこと。"""
    # Assert
    with pytest.raises(ValueError):
        Textbook.new(title=title, author_id=account_principal_id)


@pytest.mark.parametrize(
    "author_id",
    [None, 1, "not-uuid"],
    ids=INVALID_UUID_IDS,
)
def test_new_failure_invalid_author_id(textbook_title, author_id):
    """不正な著者IDでは作成できないこと。"""
    # Assert
    with pytest.raises(ValueError):
        Textbook.new(title=textbook_title, author_id=author_id)
