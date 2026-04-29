import pytest

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


def test_set_title_success_updates_title(textbook_generator):
    """タイトルを更新できること。"""

    # Arrange
    textbook = textbook_generator()
    new_title = "New Python Textbook"

    # Act
    textbook.set_title(title=new_title)

    # Assert
    assert textbook.title == new_title


def test_set_title_success_accepts_special_characters(
    textbook_generator,
    textbook_title,
):
    """記号を含む有効なタイトルに更新できること。"""

    # Arrange
    textbook = textbook_generator()

    # Act
    textbook.set_title(title=textbook_title)

    # Assert
    assert textbook.title == textbook_title


@pytest.mark.parametrize(
    "title",
    [None, 1, "", " ", "   ", "\t", "\n", " Python", "Python ", " Python "],
    ids=INVALID_TITLE_IDS,
)
def test_set_title_failure_invalid_value(textbook_generator, title):
    """不正なタイトルでは更新できないこと。"""

    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.set_title(title=title)
