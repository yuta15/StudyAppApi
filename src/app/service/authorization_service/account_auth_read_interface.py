from abc import ABC, abstractmethod
from uuid import UUID

from src.app.model.account.entities.subjects import AccountSubjects


class AccountAuthReadInterface(ABC):
    @abstractmethod
    def is_owned_subject(self, account_id:UUID, subject_type:AccountSubjects) -> bool:...
