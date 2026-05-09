from dataclasses import dataclass

from src.app.model.textbook import TextbookMetadata, TextbookSettings


@dataclass
class DeleteTextbookData:
    settings: TextbookSettings
    metadata: TextbookMetadata


class DeleteTextbookDomainService:
    @staticmethod
    def exec(delete_textbook_data: DeleteTextbookData) -> None:
        delete_textbook_data.settings.delete()
        delete_textbook_data.metadata.delete()
        return
