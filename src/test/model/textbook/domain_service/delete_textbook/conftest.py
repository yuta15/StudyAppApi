from datetime import datetime, timezone

import pytest

from src.app.model.textbook import DeleteTextbookData, Textbook, TextbookMetadata


@pytest.fixture
def textbook(textbook_id, textbook_title, account_principal_id, chapter_ids):
    return Textbook(
        textbook_id=textbook_id,
        title=textbook_title,
        author_ids=[account_principal_id],
        chapter_ids=chapter_ids,
    )


@pytest.fixture
def textbook_metadata(textbook_id, textbook_metadata_id):
    utc_now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return TextbookMetadata(
        textbook_id=textbook_id,
        metadata_id=textbook_metadata_id,
        created_at=utc_now,
        updated_at=utc_now,
    )


@pytest.fixture
def textbook_data(textbook, textbook_metadata):
    return DeleteTextbookData(
        textbook=textbook,
        metadata=textbook_metadata,
    )
