from uuid import UUID
from dataclasses import dataclass


@dataclass
class Resource:
    id:UUID
    owner: UUID
