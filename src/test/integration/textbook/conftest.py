from uuid import UUID

import pytest

from src.app.model.textbook import TitleString
from src.test import const


@pytest.fixture
def textbook_id():
    return UUID(const.textbook_id)


@pytest.fixture
def second_author_id():
    return UUID(const.textbook_second_author_id)


@pytest.fixture
def third_author_id():
    return UUID(const.textbook_third_author_id)


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
def textbook_title():
    return TitleString(const.textbook_title)


@pytest.fixture
def chapter_title():
    return TitleString(const.textbook_chapter_title)


@pytest.fixture
def chapter_content():
    return const.textbook_chapter_content
