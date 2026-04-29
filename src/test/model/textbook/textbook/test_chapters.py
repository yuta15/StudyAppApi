import pytest

from src.app.core.exceptions import DomainError

INVALID_UUID_IDS = ["none", "integer", "string"]
INVALID_CHAPTER_IDS_TYPE_IDS = ["none", "tuple", "string"]


def test_set_chapters_success_sets_chapter_ids(textbook_generator, chapter_ids):
    """章IDリストを設定できること。"""

    # Arrange
    textbook = textbook_generator()

    # Act
    textbook.set_chapters(chapter_ids=chapter_ids)

    # Assert
    assert textbook.chapter_ids == chapter_ids


def test_set_chapters_success_overwrites_chapter_ids(
    textbook_generator,
    chapter_ids,
    new_chapter_ids,
):
    """章IDリストを上書きできること。"""

    # Arrange
    textbook = textbook_generator()
    textbook.set_chapters(chapter_ids=chapter_ids)

    # Act
    textbook.set_chapters(chapter_ids=new_chapter_ids)

    # Assert
    assert textbook.chapter_ids == new_chapter_ids


def test_set_chapters_success_accepts_empty_list(textbook_generator, chapter_ids):
    """章IDリストを空に更新できること。"""

    # Arrange
    textbook = textbook_generator()
    textbook.set_chapters(chapter_ids=chapter_ids)

    # Act
    textbook.set_chapters(chapter_ids=[])

    # Assert
    assert textbook.chapter_ids == []


@pytest.mark.parametrize(
    "chapter_ids",
    [None, (), "not-list"],
    ids=INVALID_CHAPTER_IDS_TYPE_IDS,
)
def test_set_chapters_failure_invalid_chapter_ids_type(
    textbook_generator,
    chapter_ids,
):
    """list以外の章IDリストは設定できないこと。"""

    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.set_chapters(chapter_ids=chapter_ids)


@pytest.mark.parametrize(
    "chapter_id",
    [None, 1, "not-uuid"],
    ids=INVALID_UUID_IDS,
)
def test_set_chapters_failure_invalid_chapter_id(
    textbook_generator,
    chapter_id,
):
    """不正な章IDは設定できないこと。"""

    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.set_chapters(chapter_ids=[chapter_id])


def test_set_chapters_failure_duplicate_chapter_id(textbook_generator, chapter_id):
    """重複した章IDは設定できないこと。"""

    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(DomainError):
        textbook.set_chapters(chapter_ids=[chapter_id, chapter_id])
