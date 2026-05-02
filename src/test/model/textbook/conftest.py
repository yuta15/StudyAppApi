from datetime import datetime, timezone
from uuid import UUID

import pytest

from src.app.model.textbook import Textbook, TextbookMetadata, TitleString
from src.test import const


@pytest.fixture
def textbook_id():
    return UUID(const.textbook_id)


@pytest.fixture
def textbook_metadata_id():
    return UUID(const.textbook_metadata_id)


@pytest.fixture
def second_author_id():
    return UUID(const.textbook_second_author_id)


@pytest.fixture
def third_author_id():
    return UUID(const.textbook_third_author_id)


@pytest.fixture
def unregistered_author_id():
    return UUID(const.textbook_unregistered_author_id)


@pytest.fixture
def chapter_id():
    return UUID(const.textbook_chapter_id)


@pytest.fixture
def another_chapter_id():
    return UUID(const.textbook_another_chapter_id)


@pytest.fixture
def new_chapter_id():
    return UUID(const.textbook_new_chapter_id)


@pytest.fixture
def chapter_ids(chapter_id, another_chapter_id):
    return [chapter_id, another_chapter_id]


@pytest.fixture
def new_chapter_ids(new_chapter_id):
    return [new_chapter_id]


@pytest.fixture
def chapter_title():
    return TitleString(const.textbook_chapter_title)


@pytest.fixture
def chapter_content():
    return const.textbook_chapter_content


@pytest.fixture
def textbook_metadata_generator(textbook_id, textbook_metadata_id):
    def generator():
        utc_now = datetime.now(timezone.utc)
        return TextbookMetadata(
            textbook_id=textbook_id,
            metadata_id=textbook_metadata_id,
            created_at=utc_now,
            updated_at=utc_now,
        )

    return generator


@pytest.fixture
def textbook_title():
    return TitleString('Python & AI <Basics> "DDD" O\'Reilly #1: A/B')


@pytest.fixture
def textbook_generator(account_principal_id):
    def generator(title=None):
        if title is None:
            title = TitleString("Python Textbook")
        return Textbook.new(title=title, author_id=account_principal_id)

    return generator
