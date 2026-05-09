import pytest

from src.app.model.textbook import TextbookStatus

INVALID_STATUS_TYPE_IDS = ["none", "integer", "string"]


@pytest.mark.parametrize(
    "status",
    [
        TextbookStatus.DRAFT,
        TextbookStatus.IN_REVIEW,
        TextbookStatus.PUBLISHED,
        TextbookStatus.ARCHIVED,
    ],
)
def test_set_status_success_updates_status(textbook_generator, status):
    """教材ステータスをTextbookStatusに更新でき、他の値は維持されること。"""
    # Arrange
    textbook = textbook_generator()
    expected_textbook_id = textbook.textbook_id
    expected_title = textbook.title
    expected_author_ids = list(textbook.author_ids)
    expected_chapter_ids = list(textbook.chapter_ids)

    # Act
    textbook.set_status(status=status)

    # Assert
    assert textbook.status == status
    assert textbook.textbook_id == expected_textbook_id
    assert textbook.title == expected_title
    assert textbook.author_ids == expected_author_ids
    assert textbook.chapter_ids == expected_chapter_ids


@pytest.mark.parametrize(
    "status",
    [None, 1, "PUBLISHED"],
    ids=INVALID_STATUS_TYPE_IDS,
)
def test_set_status_failure_invalid_status_type(textbook_generator, status):
    """TextbookStatus以外のステータスでは更新できず、状態が維持されること。"""
    # Arrange
    textbook = textbook_generator()
    expected_status = textbook.status
    expected_textbook_id = textbook.textbook_id
    expected_title = textbook.title
    expected_author_ids = list(textbook.author_ids)
    expected_chapter_ids = list(textbook.chapter_ids)

    # Assert
    with pytest.raises(ValueError):
        textbook.set_status(status=status)
    assert textbook.status == expected_status
    assert textbook.textbook_id == expected_textbook_id
    assert textbook.title == expected_title
    assert textbook.author_ids == expected_author_ids
    assert textbook.chapter_ids == expected_chapter_ids
