import pytest

from src.app.model.textbook import Textbook


@pytest.fixture
def textbook(textbook_id, textbook_title, account_principal_id, chapter_ids):
    return Textbook(
        textbook_id=textbook_id,
        title=textbook_title,
        author_ids=[account_principal_id],
        chapter_ids=list(chapter_ids),
    )
