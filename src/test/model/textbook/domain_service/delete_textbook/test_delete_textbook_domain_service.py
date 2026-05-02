from src.app.model.textbook import DeleteTextbookDomainService


def test_exec_success_deletes_textbook_and_metadata(textbook_data):
    """教材削除時にTextbookとMetadataが削除状態になること。"""
    # Act
    DeleteTextbookDomainService.exec(delete_textbook_data=textbook_data)

    # Assert
    assert not textbook_data.textbook.is_public
    assert textbook_data.metadata.deleted_at is not None
