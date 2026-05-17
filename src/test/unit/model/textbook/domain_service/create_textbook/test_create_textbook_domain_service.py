from src.app.model.textbook import CreateTextbookDomainService, TextbookStatus


def test_exec_success_creates_textbook_metadata_and_settings(create_textbook_input):
    """教材作成時にTextbook、Metadata、Settingsが作成されること。"""
    # Act
    result = CreateTextbookDomainService.exec(create_textbook_input=create_textbook_input)

    # Assert
    assert result.textbook.title == create_textbook_input.title
    assert result.textbook.author_ids == [create_textbook_input.author_id]
    assert result.textbook.status == TextbookStatus.DRAFT
    assert result.settings.textbook_id == result.textbook.textbook_id
    assert result.settings.is_public is True
    assert result.metadata.textbook_id == result.textbook.textbook_id
