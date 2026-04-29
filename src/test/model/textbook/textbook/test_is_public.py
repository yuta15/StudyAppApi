import pytest

INVALID_IS_PUBLIC_TYPE_IDS = ["none", "integer", "string"]


@pytest.mark.parametrize(
    "is_public",
    [False, True],
    ids=["private", "public"],
)
def test_set_is_public_success_updates_is_public(
    textbook_generator,
    chapter_ids,
    is_public,
):
    """公開状態をbool値に更新でき、他の状態は維持されること。"""
    # Arrange
    textbook = textbook_generator()
    textbook.set_chapters(chapter_ids=chapter_ids)
    expected_title = textbook.title
    expected_author_ids = list(textbook.author_ids)
    expected_chapter_ids = list(textbook.chapter_ids)

    # Act
    textbook.set_is_public(is_public=is_public)

    # Assert
    assert textbook.is_public is is_public
    assert textbook.title == expected_title
    assert textbook.author_ids == expected_author_ids
    assert textbook.chapter_ids == expected_chapter_ids


@pytest.mark.parametrize(
    "is_public",
    [None, 1, "true"],
    ids=INVALID_IS_PUBLIC_TYPE_IDS,
)
def test_set_is_public_failure_invalid_is_public_type(textbook_generator, is_public):
    """bool以外の公開状態では更新できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.set_is_public(is_public=is_public)
