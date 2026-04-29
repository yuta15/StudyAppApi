from dataclasses import dataclass
from typing import Self
from uuid import UUID
from abc import ABC, abstractmethod
from enum import Enum


class PrincipalTypes(Enum):
    ACCOUNT = "ACCOUNT"


@dataclass
class Principal(ABC):
    principal_id: UUID

    @classmethod
    @abstractmethod
    def new(cls, **kwargs) -> Self: ...
