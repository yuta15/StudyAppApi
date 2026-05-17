import pytest

from src.app.core.exceptions import DataNotFoundError
from src.app.infra.textbook import ChapterRepository
from src.app.model.textbook import Chapter
from src.app.schemas.db.textbook import ChapterTable

pytestmark = pytest.mark.integration


def test_get_success_returns_chapter(
    infra_session,
    chapter_id,
    chapter_title,
    chapter_content,
):
    """DB値からTitleStringを持つChapterを復元できること。"""
    # Arrange
    infra_session.add(
        ChapterTable(
            chapter_id=chapter_id,
            title=chapter_title.value,
            content=chapter_content,
        )
    )
    infra_session.flush()
    repository = ChapterRepository(session=infra_session)

    # Act
    chapter = repository.get(chapter_id=chapter_id)

    # Assert
    assert chapter == Chapter(chapter_id=chapter_id, title=chapter_title, content=chapter_content)


def test_get_failure_missing_chapter(
    infra_session,
    chapter_id,
):
    """存在しない章の取得ではDataNotFoundErrorになること。"""
    # Arrange
    repository = ChapterRepository(session=infra_session)

    # Assert
    with pytest.raises(DataNotFoundError):
        repository.get(chapter_id=chapter_id)
