from datetime import datetime
from uuid import UUID, uuid4

from src.app.model.textbook.entities.metadata import TextbookMetadata


def test_textbook_metadata_new():
    """新規作成したTextbookMetadataに必要なIDと日時が設定されることを確認する。"""

    textbook_id = uuid4()
    metadata = TextbookMetadata.new(textbook_id=textbook_id)
    assert metadata.textbook_id == textbook_id
    assert isinstance(metadata.metadata_id, UUID)
    assert isinstance(metadata.created_at, datetime)
    assert isinstance(metadata.updated_at, datetime)
    assert metadata.deleted_at is None


def test_textbook_metadata_update():
    """更新時にupdated_atが更新されることを確認する。"""

    metadata = TextbookMetadata.new(textbook_id=uuid4())
    updated_at = metadata.updated_at
    metadata.update()
    assert metadata.updated_at >= updated_at


def test_textbook_metadata_delete():
    """削除時にdeleted_atが設定されることを確認する。"""

    metadata = TextbookMetadata.new(textbook_id=uuid4())
    metadata.delete()
    assert isinstance(metadata.deleted_at, datetime)
