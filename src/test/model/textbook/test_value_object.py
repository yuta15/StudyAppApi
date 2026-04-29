import pytest

from src.app.model.textbook.entities.value_object import TitleString


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


@pytest.mark.parametrize(
    "title",
    [
        "Python Textbook",
        'Python & AI <Basics> "DDD" O\'Reilly #1: A/B',
    ],
    ids=["plain", "special_characters"],
)
def test_title_string_success_creates_value(title):
    """有効な文字列からタイトル値を作成できること。"""
    # Act
    title_string = TitleString(title)

    # Assert
    assert title_string.value == title


@pytest.mark.parametrize(
    "title",
    [None, 1, "", " ", "   ", "\t", "\n", " Python", "Python ", " Python "],
    ids=INVALID_TITLE_IDS,
)
def test_title_string_failure_invalid_value(title):
    """不正なタイトル文字列では作成できないこと。"""
    # Assert
    with pytest.raises(ValueError):
        TitleString(title)
