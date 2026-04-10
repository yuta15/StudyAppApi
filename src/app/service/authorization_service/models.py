from enum import Enum
from dataclasses import dataclass
from uuid import UUID

from src.app.model.account.entities.subjects import AccountSubjects


@dataclass
class AccountAuthInput:
    principal_id:UUID
    subject_id:UUID
    subject_type:AccountSubjects