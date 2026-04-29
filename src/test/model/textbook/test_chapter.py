from uuid import UUID

import pytest

from src.app.model.textbook.entities.value_object import TitleString
from src.app.model.textbook.entities.subjects import Chapter

INVALID_TITLE_TYPE_IDS = ["none", "integer", "string"]
INVALID_CONTENT_TYPE_IDS = ["none", "integer", "list"]


def test_new_success_creates_empty_chapter():
    """新規作成時にIDだけが設定され、タイトルと本文は未入力状態になること。"""
    # Act
    chapter = Chapter.new()

    # Assert
    assert isinstance(chapter.chapter_id, UUID)
    assert chapter.title is None
    assert chapter.content is None


def test_set_title_success_updates_title():
    """タイトルを更新できること。"""
    # Arrange
    chapter = Chapter.new()
    new_title = TitleString("Advanced Python")

    # Act
    chapter.set_title(title=new_title)

    # Assert
    assert chapter.title == new_title
    assert chapter.content is None


@pytest.mark.parametrize(
    "title",
    [None, 1, "Python"],
    ids=INVALID_TITLE_TYPE_IDS,
)
def test_set_title_failure_invalid_title_type(title):
    """TitleString以外のタイトルでは更新できないこと。"""
    # Arrange
    chapter = Chapter.new()

    # Assert
    with pytest.raises(ValueError):
        chapter.set_title(title=title)


def test_set_content_success_updates_content(chapter_content):
    """Markdown形式の本文に更新できること。"""
    # Arrange
    chapter = Chapter.new()

    # Act
    chapter.set_content(content=chapter_content)

    # Assert
    assert chapter.content == chapter_content
    assert chapter.title is None


def test_set_content_success_accepts_empty_content():
    """本文を空文字に更新できること。"""
    # Arrange
    chapter = Chapter.new()

    # Act
    chapter.set_content(content="")

    # Assert
    assert chapter.content == ""


@pytest.mark.parametrize(
    "content",
    [None, 1, []],
    ids=INVALID_CONTENT_TYPE_IDS,
)
def test_set_content_failure_invalid_content_type(content):
    """文字列以外の本文では更新できないこと。"""
    # Arrange
    chapter = Chapter.new()

    # Assert
    with pytest.raises(ValueError):
        chapter.set_content(content=content)
