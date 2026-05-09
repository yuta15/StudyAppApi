from uuid import UUID
from dataclasses import dataclass

from src.app.model.textbook.entities.value_object import TextbookStatus, TitleString
from src.app.service.domain_read_service.interface.textbook import (
    MinimalReadTextbookMetadata,
    MinimalReadTextbookSettings,
    MinimalReadChapter,
)
from src.app.service.domain_read_service.interface.account import ReadMinimalAccount


@dataclass
class ReadTextbookDetailsModel:
    textbook_id: UUID
    title: TitleString
    status: TextbookStatus
    authors: list[ReadMinimalAccount]
    chapters: list[MinimalReadChapter]
    settings: MinimalReadTextbookSettings
    metadata: MinimalReadTextbookMetadata
