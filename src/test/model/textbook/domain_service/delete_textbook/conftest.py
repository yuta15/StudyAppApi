import pytest

from src.app.model.textbook import DeleteTextbookData


@pytest.fixture
def textbook_data(textbook_settings, textbook_metadata):
    return DeleteTextbookData(
        settings=textbook_settings,
        metadata=textbook_metadata,
    )
