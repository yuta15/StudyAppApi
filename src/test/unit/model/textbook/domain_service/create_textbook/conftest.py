import pytest

from src.app.model.textbook import CreateTextbookInput


@pytest.fixture
def create_textbook_input(textbook_title, account_principal_id):
    return CreateTextbookInput(
        title=textbook_title,
        author_id=account_principal_id,
    )
