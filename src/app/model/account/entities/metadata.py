from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Self
from uuid import uuid4, UUID


@dataclass
class AccountMetadata:
    principal_id: UUID
    metadata_id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    @classmethod
    def new(cls, principal_id: UUID) -> Self:
        utc_now = datetime.now(timezone.utc)
        return AccountMetadata(
            principal_id=principal_id,
            metadata_id=uuid4(),
            created_at=utc_now,
            updated_at=utc_now,
        )

    def update(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.updated_at = utc_now

    def delete(self) -> None:
        utc_now = datetime.now(timezone.utc)
        self.deleted_at = utc_now
