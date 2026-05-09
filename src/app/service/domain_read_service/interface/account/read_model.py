from dataclasses import dataclass
from uuid import UUID

from src.app.model.account import AccountNameStrings


@dataclass
class ReadMinimalAccount:
    principal_id: UUID
    account_name: AccountNameStrings
