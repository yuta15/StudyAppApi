from src.app.model.textbook.service.create_textbook_domain_service import CreateTextbookDomainService


def test_exec_success_creates_textbook_and_metadata(create_textbook_input):
    """教材作成時にTextbookと紐づくMetadataが作成されること。"""
    # Act
    result = CreateTextbookDomainService.exec(create_textbook_input=create_textbook_input)

    # Assert
    assert result.textbook.title == create_textbook_input.title
    assert result.textbook.author_ids == [create_textbook_input.author_id]
    assert result.metadata.textbook_id == result.textbook.textbook_id
