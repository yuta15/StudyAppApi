from dataclasses import dataclass

from src.app.model.textbook.entities.metadata import TextbookMetadata
from src.app.model.textbook.entities.subjects import Textbook


@dataclass
class DeleteTextbookData:
    textbook: Textbook
    metadata: TextbookMetadata


class DeleteTextbookDomainService:
    @staticmethod
    def exec(delete_textbook_data: DeleteTextbookData) -> None:
        delete_textbook_data.textbook.delete()
        delete_textbook_data.metadata.delete()
        return
