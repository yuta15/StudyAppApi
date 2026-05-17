import pytest

from src.app.infra.textbook import TextbookRepository
from src.app.model.account import AccountStatus
from src.app.model.textbook import Textbook, TextbookStatus
from src.app.schemas.db.account import AccountTable
from src.app.schemas.db.textbook import ChapterTable, TextbookAuthorTable, TextbookChapterTable, TextbookTable

pytestmark = pytest.mark.integration


def test_get_success_reconstructs_textbook_aggregate(
    infra_session,
    textbook_id,
    textbook_title,
    account_principal_id,
    second_author_id,
    chapter_id,
    another_chapter_id,
    chapter_title,
):
    """著者と章順を含むTextbook集約を復元できること。"""
    # Arrange
    infra_session.add_all(
        [
            AccountTable(
                principal_id=account_principal_id,
                account_name="first_author",
                status=AccountStatus.ACTIVE,
            ),
            AccountTable(
                principal_id=second_author_id,
                account_name="second_author",
                status=AccountStatus.ACTIVE,
            ),
            TextbookTable(textbook_id=textbook_id, title=textbook_title.value, status=TextbookStatus.DRAFT),
            ChapterTable(chapter_id=chapter_id, title=chapter_title.value, content="chapter-1"),
            ChapterTable(chapter_id=another_chapter_id, title=chapter_title.value, content="chapter-2"),
        ]
    )
    infra_session.flush()
    infra_session.add_all(
        [
            TextbookAuthorTable(textbook_id=textbook_id, principal_id=account_principal_id),
            TextbookAuthorTable(textbook_id=textbook_id, principal_id=second_author_id),
            TextbookChapterTable(textbook_id=textbook_id, chapter_id=another_chapter_id, position=1),
            TextbookChapterTable(textbook_id=textbook_id, chapter_id=chapter_id, position=0),
        ]
    )
    infra_session.flush()
    repository = TextbookRepository(session=infra_session)

    # Act
    textbook = repository.get(textbook_id=textbook_id)

    # Assert
    assert textbook.textbook_id == textbook_id
    assert textbook.title == textbook_title
    assert textbook.author_ids == [account_principal_id, second_author_id]
    assert textbook.chapter_ids == [chapter_id, another_chapter_id]
    assert textbook.status == TextbookStatus.DRAFT


def test_save_success_syncs_textbook_relations(
    infra_session,
    textbook_id,
    textbook_title,
    account_principal_id,
    second_author_id,
    third_author_id,
    chapter_id,
    another_chapter_id,
    new_chapter_id,
    chapter_title,
):
    """Textbook保存時に著者と章の追加・削除・並び替えが同期されること。"""
    # Arrange
    infra_session.add_all(
        [
            AccountTable(
                principal_id=account_principal_id,
                account_name="first_author",
                status=AccountStatus.ACTIVE,
            ),
            AccountTable(
                principal_id=second_author_id,
                account_name="second_author",
                status=AccountStatus.ACTIVE,
            ),
            AccountTable(
                principal_id=third_author_id,
                account_name="third_author",
                status=AccountStatus.ACTIVE,
            ),
            TextbookTable(textbook_id=textbook_id, title="old title", status=TextbookStatus.DRAFT),
            ChapterTable(chapter_id=chapter_id, title=chapter_title.value, content="chapter-1"),
            ChapterTable(chapter_id=another_chapter_id, title=chapter_title.value, content="chapter-2"),
            ChapterTable(chapter_id=new_chapter_id, title=chapter_title.value, content="chapter-3"),
        ]
    )
    infra_session.flush()
    infra_session.add_all(
        [
            TextbookAuthorTable(textbook_id=textbook_id, principal_id=account_principal_id),
            TextbookAuthorTable(textbook_id=textbook_id, principal_id=second_author_id),
            TextbookChapterTable(textbook_id=textbook_id, chapter_id=chapter_id, position=0),
            TextbookChapterTable(textbook_id=textbook_id, chapter_id=another_chapter_id, position=1),
        ]
    )
    infra_session.flush()
    repository = TextbookRepository(session=infra_session)
    textbook = Textbook(
        textbook_id=textbook_id,
        title=textbook_title,
        author_ids=[account_principal_id, third_author_id],
        chapter_ids=[another_chapter_id, new_chapter_id],
        status=TextbookStatus.PUBLISHED,
    )

    # Act
    repository.save(textbook=textbook)
    infra_session.flush()
    saved_textbook = repository.get(textbook_id=textbook_id)

    # Assert
    assert saved_textbook.title == textbook_title
    assert saved_textbook.status == TextbookStatus.PUBLISHED
    assert saved_textbook.author_ids == [account_principal_id, third_author_id]
    assert saved_textbook.chapter_ids == [another_chapter_id, new_chapter_id]
