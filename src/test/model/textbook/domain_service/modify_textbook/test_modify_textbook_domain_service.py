import pytest

from src.app.core.exceptions import DomainError
from src.app.model.textbook import Chapter, ModifyTextbookDomainService, TitleString


@pytest.mark.parametrize(
    ("title", "is_public"),
    [
        (TitleString("Advanced Python"), None),
        (None, False),
        (TitleString("Advanced Python"), False),
    ],
    ids=["title", "is_public", "title_and_is_public"],
)
def test_update_textbook_success_updates_changed_values(textbook, textbook_metadata, title, is_public):
    """教材のタイトル・公開状態に変更がある場合、対象項目とmetadataが更新されること。"""
    # Arrange
    updated_at = textbook_metadata.updated_at
    expected_title = textbook.title if title is None else title
    expected_is_public = textbook.is_public if is_public is None else is_public

    # Act
    is_changed = ModifyTextbookDomainService.update_textbook(
        textbook=textbook,
        metadata=textbook_metadata,
        title=title,
        is_public=is_public,
    )

    # Assert
    assert is_changed
    assert textbook.title == expected_title
    assert textbook.is_public == expected_is_public
    assert textbook_metadata.updated_at != updated_at


@pytest.mark.parametrize(
    "case",
    [
        "no_values",
        "same_title",
        "same_is_public",
        "same_title_and_is_public",
    ],
)
def test_update_textbook_success_no_change(textbook, textbook_metadata, case):
    """教材に実際の変更がない場合、metadataが更新されずFalseが返ること。"""
    # Arrange
    values = {
        "no_values": {},
        "same_title": {"title": textbook.title},
        "same_is_public": {"is_public": textbook.is_public},
        "same_title_and_is_public": {
            "title": textbook.title,
            "is_public": textbook.is_public,
        },
    }[case]
    title = textbook.title
    is_public = textbook.is_public
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
    assert textbook.is_public == is_public
    assert textbook_metadata.updated_at == updated_at


def test_update_textbook_success_updates_only_different_field(textbook, textbook_metadata):
    """同じタイトルと変更された公開状態を渡した場合、変更された公開状態だけ更新されること。"""
    # Arrange
    title = textbook.title
    updated_at = textbook_metadata.updated_at

    # Act
    is_changed = ModifyTextbookDomainService.update_textbook(
        textbook=textbook,
        metadata=textbook_metadata,
        title=title,
        is_public=False,
    )

    # Assert
    assert is_changed
    assert textbook.title == title
    assert not textbook.is_public
    assert textbook_metadata.updated_at != updated_at


@pytest.mark.parametrize(
    "values",
    [
        {"title": "Advanced Python"},
        {"is_public": "false"},
    ],
    ids=["title", "is_public"],
)
def test_update_textbook_failure_invalid_value_propagates_from_entity(textbook, textbook_metadata, values):
    """型不正の場合、Entityの検証例外が伝播しmetadataが更新されないこと。"""
    # Arrange
    title = textbook.title
    is_public = textbook.is_public
    updated_at = textbook_metadata.updated_at

    # Assert
    with pytest.raises(ValueError):
        ModifyTextbookDomainService.update_textbook(
            textbook=textbook,
            metadata=textbook_metadata,
            **values,
        )
    assert textbook.title == title
    assert textbook.is_public == is_public
    assert textbook_metadata.updated_at == updated_at


def test_add_chapter_success_creates_empty_chapter_and_appends_id(textbook, textbook_metadata):
    """未入力状態のChapterを作成し、chapter_idがTextbookの末尾に追加されること。"""
    # Arrange
    chapter_ids = list(textbook.chapter_ids)
    updated_at = textbook_metadata.updated_at

    # Act
    chapter = ModifyTextbookDomainService.add_chapter(
        textbook=textbook,
        metadata=textbook_metadata,
    )

    # Assert
    assert isinstance(chapter, Chapter)
    assert chapter.title is None
    assert chapter.content is None
    assert textbook.chapter_ids == [*chapter_ids, chapter.chapter_id]
    assert textbook_metadata.updated_at != updated_at


def test_add_chapter_failure_chapter_creation_error(textbook, textbook_metadata, mocker):
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
