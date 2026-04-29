from datetime import datetime, timezone

import pytest

from src.app.model.textbook.entities.metadata import TextbookMetadata
from src.app.model.textbook.entities.subjects import Textbook
from src.app.model.textbook.service.delete_textbook_domain_service import DeleteTextbookData


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
