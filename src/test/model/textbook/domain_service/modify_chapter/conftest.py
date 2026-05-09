import pytest

from src.app.model.textbook import Chapter


@pytest.fixture
def chapter(chapter_id, chapter_title, chapter_content):
    return Chapter(
        chapter_id=chapter_id,
        title=chapter_title,
        content=chapter_content,
    )


@pytest.fixture
def empty_chapter(chapter_id):
    return Chapter(chapter_id=chapter_id)
