from uuid import UUID

import pytest

from src.app.model.textbook.entities.value_object import TitleString
from src.app.model.textbook.entities.subjects import Chapter

INVALID_TITLE_TYPE_IDS = ["none", "integer", "string"]
INVALID_CONTENT_TYPE_IDS = ["none", "integer", "list"]


def test_new_success_creates_chapter(chapter_title, chapter_content):
    """新規作成時にID、タイトル、本文が設定されること。"""

    # Act
    chapter = Chapter.new(title=chapter_title, content=chapter_content)

    # Assert
    assert isinstance(chapter.chapter_id, UUID)
    assert chapter.title == chapter_title
    assert chapter.content == chapter_content


def test_new_success_accepts_empty_content(chapter_title):
    """本文が空文字でも作成できること。"""

    # Act
    chapter = Chapter.new(title=chapter_title, content="")

    # Assert
    assert chapter.content == ""


@pytest.mark.parametrize(
    "title",
    [None, 1, "Python"],
    ids=INVALID_TITLE_TYPE_IDS,
)
def test_new_failure_invalid_title_type(title, chapter_content):
    """TitleString以外のタイトルでは作成できないこと。"""

    # Assert
    with pytest.raises(ValueError):
        Chapter.new(title=title, content=chapter_content)


@pytest.mark.parametrize(
    "content",
    [None, 1, []],
    ids=INVALID_CONTENT_TYPE_IDS,
)
def test_new_failure_invalid_content_type(chapter_title, content):
    """文字列以外の本文では作成できないこと。"""

    # Assert
    with pytest.raises(ValueError):
        Chapter.new(title=chapter_title, content=content)


def test_set_title_success_updates_title(chapter_title, chapter_content):
    """タイトルを更新できること。"""

    # Arrange
    chapter = Chapter.new(title=chapter_title, content=chapter_content)
    new_title = TitleString("Advanced Python")

    # Act
    chapter.set_title(title=new_title)

    # Assert
    assert chapter.title == new_title
    assert chapter.content == chapter_content


@pytest.mark.parametrize(
    "title",
    [None, 1, "Python"],
    ids=INVALID_TITLE_TYPE_IDS,
)
def test_set_title_failure_invalid_title_type(chapter_title, chapter_content, title):
    """TitleString以外のタイトルでは更新できないこと。"""

    # Arrange
    chapter = Chapter.new(title=chapter_title, content=chapter_content)

    # Assert
    with pytest.raises(ValueError):
        chapter.set_title(title=title)


def test_set_content_success_updates_content(chapter_title, chapter_content):
    """Markdown形式の本文に更新できること。"""

    # Arrange
    chapter = Chapter.new(title=chapter_title, content="")

    # Act
    chapter.set_content(content=chapter_content)

    # Assert
    assert chapter.content == chapter_content
    assert chapter.title == chapter_title


def test_set_content_success_accepts_empty_content(chapter_title, chapter_content):
    """本文を空文字に更新できること。"""

    # Arrange
    chapter = Chapter.new(title=chapter_title, content=chapter_content)

    # Act
    chapter.set_content(content="")

    # Assert
    assert chapter.content == ""


@pytest.mark.parametrize(
    "content",
    [None, 1, []],
    ids=INVALID_CONTENT_TYPE_IDS,
)
def test_set_content_failure_invalid_content_type(chapter_title, chapter_content, content):
    """文字列以外の本文では更新できないこと。"""

    # Arrange
    chapter = Chapter.new(title=chapter_title, content=chapter_content)

    # Assert
    with pytest.raises(ValueError):
        chapter.set_content(content=content)
