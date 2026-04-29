from datetime import datetime, timezone

import pytest

from src.app.model.textbook.entities.metadata import TextbookMetadata
from src.app.model.textbook.entities.subjects import Chapter


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


@pytest.fixture
def textbook_metadata(textbook_id, textbook_metadata_id):
    utc_now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return TextbookMetadata(
        textbook_id=textbook_id,
        metadata_id=textbook_metadata_id,
        created_at=utc_now,
        updated_at=utc_now,
    )
