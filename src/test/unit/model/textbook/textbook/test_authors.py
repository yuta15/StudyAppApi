import pytest

from src.app.core.exceptions import DomainError

INVALID_UUID_IDS = ["none", "integer", "string"]


def test_add_author_success_appends_author_id(
    textbook_generator,
    account_principal_id,
    second_author_id,
):
    """新しい著者IDを末尾に追加できること。"""
    # Arrange
    textbook = textbook_generator()

    # Act
    textbook.add_author(author_id=second_author_id)

    # Assert
    assert textbook.author_ids == [account_principal_id, second_author_id]


def test_add_author_success_preserves_added_order(
    textbook_generator,
    account_principal_id,
    second_author_id,
    third_author_id,
):
    """複数の著者IDを追加順で保持すること。"""
    # Arrange
    textbook = textbook_generator()

    # Act
    textbook.add_author(author_id=second_author_id)
    textbook.add_author(author_id=third_author_id)

    # Assert
    assert textbook.author_ids == [
        account_principal_id,
        second_author_id,
        third_author_id,
    ]


@pytest.mark.parametrize(
    "author_id",
    [None, 1, "not-uuid"],
    ids=INVALID_UUID_IDS,
)
def test_add_author_failure_invalid_author_id(textbook_generator, author_id):
    """不正な著者IDは追加できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.add_author(author_id=author_id)


def test_add_author_failure_duplicate_author_id(
    textbook_generator,
    account_principal_id,
):
    """登録済み著者IDは重複追加できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(DomainError):
        textbook.add_author(author_id=account_principal_id)


def test_remove_author_success_removes_registered_author(
    textbook_generator,
    account_principal_id,
    second_author_id,
):
    """登録済み著者IDを削除できること。"""
    # Arrange
    textbook = textbook_generator()
    textbook.add_author(author_id=second_author_id)

    # Act
    textbook.remove_author(author_id=second_author_id)

    # Assert
    assert textbook.author_ids == [account_principal_id]


def test_remove_author_success_removes_initial_author_when_another_exists(
    textbook_generator,
    second_author_id,
):
    """他の著者がいる場合は初期著者を削除できること。"""
    # Arrange
    textbook = textbook_generator()
    initial_author_id = textbook.author_ids[0]
    textbook.add_author(author_id=second_author_id)

    # Act
    textbook.remove_author(author_id=initial_author_id)

    # Assert
    assert textbook.author_ids == [second_author_id]


@pytest.mark.parametrize(
    "author_id",
    [None, 1, "not-uuid"],
    ids=INVALID_UUID_IDS,
)
def test_remove_author_failure_invalid_author_id(textbook_generator, author_id):
    """不正な著者IDは削除できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(ValueError):
        textbook.remove_author(author_id=author_id)


def test_remove_author_failure_not_registered(
    textbook_generator,
    unregistered_author_id,
):
    """未登録の著者IDは削除できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(DomainError):
        textbook.remove_author(author_id=unregistered_author_id)


def test_remove_author_failure_last_author(textbook_generator, account_principal_id):
    """最後の著者は削除できないこと。"""
    # Arrange
    textbook = textbook_generator()

    # Assert
    with pytest.raises(DomainError):
        textbook.remove_author(author_id=account_principal_id)
