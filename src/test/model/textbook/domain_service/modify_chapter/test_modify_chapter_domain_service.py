import pytest

from src.app.model.textbook.entities.value_object import TitleString
from src.app.model.textbook.service.modify_chapter_domain_service import ModifyChapterDomainService


@pytest.mark.parametrize(
    ("title", "content"),
    [
        (TitleString("Advanced Python"), None),
        (None, "# Advanced\n\n- Python typing"),
        (TitleString("Advanced Python"), "# Advanced\n\n- Python typing"),
    ],
    ids=["title", "content", "title_and_content"],
)
def test_update_chapter_success_updates_changed_values(
    chapter,
    textbook_metadata,
    title,
    content,
):
    """Chapterのタイトル・本文に変更がある場合、対象項目とmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at
    expected_title = chapter.title if title is None else title
    expected_content = chapter.content if content is None else content

    # Act
    is_changed = ModifyChapterDomainService.update_chapter(
        chapter=chapter,
        metadata=textbook_metadata,
        title=title,
        content=content,
    )

    # Assert
    assert is_changed
    assert chapter.title == expected_title
    assert chapter.content == expected_content
    assert textbook_metadata.updated_at != updated_at


@pytest.mark.parametrize(
    ("title", "content"),
    [
        (TitleString("Advanced Python"), None),
        (None, "# Advanced\n\n- Python typing"),
        (TitleString("Advanced Python"), "# Advanced\n\n- Python typing"),
    ],
    ids=["title", "content", "title_and_content"],
)
def test_update_chapter_success_updates_unset_values(
    empty_chapter,
    textbook_metadata,
    title,
    content,
):
    """未設定のタイトル・本文に値を渡した場合、対象項目とmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at

    # Act
    is_changed = ModifyChapterDomainService.update_chapter(
        chapter=empty_chapter,
        metadata=textbook_metadata,
        title=title,
        content=content,
    )

    # Assert
    assert is_changed
    assert empty_chapter.title == title
    assert empty_chapter.content == content
    assert textbook_metadata.updated_at != updated_at


@pytest.mark.parametrize(
    "case",
    [
        "no_values",
        "same_title",
        "same_content",
        "same_title_and_content",
    ],
)
def test_update_chapter_success_no_change(chapter, textbook_metadata, case):
    """Chapterに実際の変更がない場合、metadataが更新されずFalseが返ること。"""
    # Arrange
    values = {
        "no_values": {},
        "same_title": {"title": chapter.title},
        "same_content": {"content": chapter.content},
        "same_title_and_content": {
            "title": chapter.title,
            "content": chapter.content,
        },
    }[case]
    title = chapter.title
    content = chapter.content
    updated_at = textbook_metadata.updated_at

    # Act
    is_changed = ModifyChapterDomainService.update_chapter(
        chapter=chapter,
        metadata=textbook_metadata,
        **values,
    )

    # Assert
    assert not is_changed
    assert chapter.title == title
    assert chapter.content == content
    assert textbook_metadata.updated_at == updated_at


def test_update_chapter_success_updates_content_to_empty_string(empty_chapter, textbook_metadata):
    """本文が未設定のChapterでも、空文字を有効な本文として更新できること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at

    # Act
    is_changed = ModifyChapterDomainService.update_chapter(
        chapter=empty_chapter,
        metadata=textbook_metadata,
        content="",
    )

    # Assert
    assert is_changed
    assert empty_chapter.content == ""
    assert textbook_metadata.updated_at != updated_at


def test_update_chapter_failure_invalid_content_does_not_update_chapter_or_metadata(chapter, textbook_metadata):
    """一部の値が不正な場合、Chapterとmetadataが更新されないこと。"""
    # Arrange
    title = chapter.title
    content = chapter.content
    updated_at = textbook_metadata.updated_at

    # Assert
    with pytest.raises(ValueError):
        ModifyChapterDomainService.update_chapter(
            chapter=chapter,
            metadata=textbook_metadata,
            title=TitleString("Advanced Python"),
            content=1,
        )
    assert chapter.title == title
    assert chapter.content == content
    assert textbook_metadata.updated_at == updated_at
