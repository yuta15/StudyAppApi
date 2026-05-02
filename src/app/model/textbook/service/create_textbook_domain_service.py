from dataclasses import dataclass
from uuid import UUID

from src.app.model.textbook import Textbook, TextbookMetadata, TitleString


@dataclass
class CreateTextbookInput:
    title: TitleString
    author_id: UUID


@dataclass
class CreateTextbookOutput:
    textbook: Textbook
    metadata: TextbookMetadata


class CreateTextbookDomainService:
    @staticmethod
    def exec(create_textbook_input: CreateTextbookInput) -> CreateTextbookOutput:
        textbook = Textbook.new(title=create_textbook_input.title, author_id=create_textbook_input.author_id)
        return CreateTextbookOutput(textbook=textbook, metadata=TextbookMetadata.new(textbook_id=textbook.textbook_id))
