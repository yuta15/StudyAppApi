import pytest

from src.app.model.textbook.entities.value_object import TitleString

INVALID_TITLE_TYPE_IDS = ["none", "integer", "string"]


def test_set_title_success_updates_title(textbook_generator):
    """タイトルを更新できること。"""
    # Arrange
    textbook = textbook_generator()
    new_title = TitleString("New Python Textbook")

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
    [None, 1, "Python"],
    ids=INVALID_TITLE_TYPE_IDS,
)
def test_set_title_failure_invalid_title_type(textbook_generator, title):
    """TitleString以外のタイトルでは更新できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.set_title(title=title)
