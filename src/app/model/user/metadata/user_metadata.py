from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Self


@dataclass
class UserMetadata:
    created_at:datetime 
    updated_at:datetime
    deleted_at:datetime | None = None

    @classmethod
    def new(cls) -> Self:
        utc_now = datetime.now(timezone.utc)
        return UserMetadata(
            created_at=utc_now,
            updated_at=utc_now,
            deleted_at=None
        )

    def delete(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.deleted_at = utc_now

    def update(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.updated_at = utc_now