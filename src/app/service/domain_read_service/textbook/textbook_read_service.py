from uuid import UUID

from src.app.service.interface.account import AccountReadInterface
from src.app.service.interface.textbook import TextbookReadInterface
from src.app.service.domain_read_service.textbook.models import ReadTextbookDetailsModel


class TextbookReadService:
    def __init__(self, account_read: AccountReadInterface, textbook_read: TextbookReadInterface):
        self._account_read = account_read
        self._textbook_read = textbook_read

    def get_textbook_details(self, textbook_id: UUID) -> ReadTextbookDetailsModel:
        textbook = self._textbook_read.fetch_textbook(textbook_id=textbook_id)
        authors = self._account_read.fetch_minimal_accounts(principal_ids=textbook.author_ids)

        return ReadTextbookDetailsModel(
            textbook_id=textbook.textbook_id,
            title=textbook.title,
            status=textbook.status,
            authors=authors,
            chapters=textbook.chapters,
            metadata=textbook.metadata,
        )
