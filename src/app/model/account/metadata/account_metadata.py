from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Self


@dataclass
class AccountMetadata:
    created_at:datetime 
    updated_at:datetime

    @classmethod
    def new(cls) -> Self:
        utc_now = datetime.now(timezone.utc)
        return AccountMetadata(
            created_at=utc_now,
            updated_at=utc_now,
        )

    def update(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.updated_at = utc_now