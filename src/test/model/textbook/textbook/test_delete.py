def test_delete_success_makes_textbook_private(textbook_generator):
    """削除時に教材が非公開になること。"""
    # Arrange
    textbook = textbook_generator()
    textbook.set_is_public(is_public=True)

    # Act
    textbook.delete()

    # Assert
    assert textbook.is_public is False


def test_delete_success_preserves_textbook_attributes(
    textbook_generator,
    chapter_ids,
    second_author_id,
):
    """削除時に公開状態以外の教材情報は維持されること。"""
    # Arrange
    textbook = textbook_generator()
    textbook.add_author(author_id=second_author_id)
    textbook.set_chapters(chapter_ids=chapter_ids)
    expected_textbook_id = textbook.textbook_id
    expected_title = textbook.title
    expected_author_ids = list(textbook.author_ids)
    expected_chapter_ids = list(textbook.chapter_ids)

    # Act
    textbook.delete()

    # Assert
    assert textbook.textbook_id == expected_textbook_id
    assert textbook.title == expected_title
    assert textbook.author_ids == expected_author_ids
    assert textbook.chapter_ids == expected_chapter_ids


def test_delete_success_keeps_private_textbook_private(textbook_generator):
    """非公開の教材も削除でき、非公開のまま維持されること。"""
    # Arrange
    textbook = textbook_generator()
    textbook.set_is_public(is_public=False)

    # Act
    textbook.delete()

    # Assert
    assert textbook.is_public is False
