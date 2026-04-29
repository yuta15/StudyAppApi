from uuid import UUID

import pytest

from src.app.model.textbook.entities.subjects import Textbook

INVALID_TITLE_IDS = [
    "none",
    "integer",
    "empty",
    "space",
    "spaces",
    "tab",
    "newline",
    "leading_space",
    "trailing_space",
    "surrounding_space",
]
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


@pytest.mark.parametrize(
    "title",
    [None, 1, "", " ", "   ", "\t", "\n", " Python", "Python ", " Python "],
    ids=INVALID_TITLE_IDS,
)
def test_new_failure_invalid_title(title, account_principal_id):
    """不正なタイトルでは作成できないこと。"""

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
