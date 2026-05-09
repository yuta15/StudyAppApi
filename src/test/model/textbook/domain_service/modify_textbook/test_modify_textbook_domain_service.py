import pytest

from src.app.core.exceptions import DomainError
from src.app.model.textbook import Chapter, ModifyTextbookDomainService, TextbookStatus, TitleString


@pytest.mark.parametrize(
    "title",
    [
        TitleString("Advanced Python"),
    ],
)
def test_update_textbook_success_updates_changed_title(textbook, textbook_metadata, title):
    """教材のタイトルに変更がある場合、タイトルとmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at
    expected_textbook_id = textbook.textbook_id
    expected_status = textbook.status

    # Act
    is_changed = ModifyTextbookDomainService.update_textbook(
        textbook=textbook,
        metadata=textbook_metadata,
        title=title,
    )

    # Assert
    assert is_changed
    assert textbook.title == title
    assert textbook.status == expected_status
    assert textbook.textbook_id == expected_textbook_id
    assert textbook_metadata.updated_at != updated_at


def test_update_textbook_success_updates_changed_status(textbook, textbook_metadata):
    """教材ステータスに変更がある場合、ステータスとmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at
    expected_title = textbook.title
    expected_status = TextbookStatus.IN_REVIEW

    # Act
    is_changed = ModifyTextbookDomainService.update_textbook(
        textbook=textbook,
        metadata=textbook_metadata,
        status=expected_status,
    )

    # Assert
    assert is_changed
    assert textbook.title == expected_title
    assert textbook.status == expected_status
    assert textbook_metadata.updated_at != updated_at


def test_update_textbook_success_updates_changed_title_and_status(textbook, textbook_metadata):
    """教材のタイトルとステータスに変更がある場合、両方とmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at
    expected_title = TitleString("Advanced Python")
    expected_status = TextbookStatus.IN_REVIEW

    # Act
    is_changed = ModifyTextbookDomainService.update_textbook(
        textbook=textbook,
        metadata=textbook_metadata,
        title=expected_title,
        status=expected_status,
    )

    # Assert
    assert is_changed
    assert textbook.title == expected_title
    assert textbook.status == expected_status
    assert textbook_metadata.updated_at != updated_at


@pytest.mark.parametrize(
    "case",
    [
        "no_values",
        "same_title",
        "same_status",
    ],
)
def test_update_textbook_success_no_change(textbook, textbook_metadata, case):
    """教材に実際の変更がない場合、metadataが更新されずFalseが返ること。"""
    # Arrange
    values = {
        "no_values": {},
        "same_title": {"title": textbook.title},
        "same_status": {"status": textbook.status},
    }[case]
    title = textbook.title
    status = textbook.status
    expected_textbook_id = textbook.textbook_id
    updated_at = textbook_metadata.updated_at

    # Act
    is_changed = ModifyTextbookDomainService.update_textbook(
        textbook=textbook,
        metadata=textbook_metadata,
        **values,
    )

    # Assert
    assert not is_changed
    assert textbook.title == title
    assert textbook.status == status
    assert textbook.textbook_id == expected_textbook_id
    assert textbook_metadata.updated_at == updated_at


@pytest.mark.parametrize(
    "values",
    [
        {"title": "Advanced Python"},
        {"status": "PUBLISHED"},
    ],
    ids=["title", "status"],
)
def test_update_textbook_failure_invalid_value_propagates_from_entity(textbook, textbook_metadata, values):
    """型不正の場合、Entityの検証例外が伝播しmetadataが更新されないこと。"""
    # Arrange
    title = textbook.title
    status = textbook.status
    expected_textbook_id = textbook.textbook_id
    updated_at = textbook_metadata.updated_at

    # Assert
    with pytest.raises(ValueError):
        ModifyTextbookDomainService.update_textbook(
            textbook=textbook,
            metadata=textbook_metadata,
            **values,
        )
    assert textbook.title == title
    assert textbook.status == status
    assert textbook.textbook_id == expected_textbook_id
    assert textbook_metadata.updated_at == updated_at


def test_add_chapter_success_creates_chapter_and_appends_id(textbook, textbook_metadata, chapter_title):
    """タイトル付きのChapterを作成し、chapter_idがTextbookの末尾に追加されること。"""
    # Arrange
    chapter_ids = list(textbook.chapter_ids)
    updated_at = textbook_metadata.updated_at

    # Act
    chapter = ModifyTextbookDomainService.add_chapter(
        textbook=textbook,
        metadata=textbook_metadata,
        title=chapter_title,
    )

    # Assert
    assert isinstance(chapter, Chapter)
    assert chapter.title == chapter_title
    assert chapter.content == ""
    assert textbook.chapter_ids == [*chapter_ids, chapter.chapter_id]
    assert textbook_metadata.updated_at != updated_at


def test_add_chapter_failure_chapter_creation_error(textbook, textbook_metadata, chapter_title, mocker):
    """Chapter作成に失敗した場合、例外が伝播しTextbookとmetadataが更新されないこと。"""
    # Arrange
    chapter_ids = list(textbook.chapter_ids)
    updated_at = textbook_metadata.updated_at
    mocker.patch.object(Chapter, "new", side_effect=ValueError)

    # Assert
    with pytest.raises(ValueError):
        ModifyTextbookDomainService.add_chapter(
            textbook=textbook,
            metadata=textbook_metadata,
            title=chapter_title,
        )
    assert textbook.chapter_ids == chapter_ids
    assert textbook_metadata.updated_at == updated_at


def test_remove_chapter_success_removes_existing_chapter_id(
    textbook,
    textbook_metadata,
    chapter_id,
    another_chapter_id,
):
    """登録済みのchapter_idを削除し、残りのchapter_idsの順序が維持されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at

    # Act
    is_removed = ModifyTextbookDomainService.remove_chapter(
        textbook=textbook,
        metadata=textbook_metadata,
        chapter_id=chapter_id,
    )

    # Assert
    assert is_removed
    assert textbook.chapter_ids == [another_chapter_id]
    assert textbook_metadata.updated_at != updated_at


def test_remove_chapter_success_allows_removing_last_chapter(
    textbook,
    textbook_metadata,
    chapter_id,
):
    """最後のChapterを削除でき、chapter_idsが空配列になること。"""
    # Arrange
    textbook.set_chapters(chapter_ids=[chapter_id])
    updated_at = textbook_metadata.updated_at

    # Act
    is_removed = ModifyTextbookDomainService.remove_chapter(
        textbook=textbook,
        metadata=textbook_metadata,
        chapter_id=chapter_id,
    )

    # Assert
    assert is_removed
    assert textbook.chapter_ids == []
    assert textbook_metadata.updated_at != updated_at


def test_remove_chapter_failure_not_registered_chapter_id(
    textbook,
    textbook_metadata,
    new_chapter_id,
):
    """未登録のchapter_idを削除しようとした場合、DomainErrorになりmetadataが更新されないこと。"""
    # Arrange
    chapter_ids = list(textbook.chapter_ids)
    updated_at = textbook_metadata.updated_at

    # Assert
    with pytest.raises(DomainError):
        ModifyTextbookDomainService.remove_chapter(
            textbook=textbook,
            metadata=textbook_metadata,
            chapter_id=new_chapter_id,
        )
    assert textbook.chapter_ids == chapter_ids
    assert textbook_metadata.updated_at == updated_at
